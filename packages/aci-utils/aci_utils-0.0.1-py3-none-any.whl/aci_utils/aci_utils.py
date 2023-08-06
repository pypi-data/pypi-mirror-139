#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import logging
import os
import yaml
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from endika_utils.validator_model_utils import validate_dict
logger = logging.getLogger(__name__)


class ACIObject:

    def __init__(self, url_base, admin_name, password):
        self.url_base = url_base
        self.admin_name = admin_name
        self.password = password
        self._token = self.get_token()

    def __str__(self):
        return f"""
      ACI Object Instance:
          URL_base: {self.url_base}
          Admin_name: {self.admin_name}
          Pass: ********
          Token: {self._token}
      """

    def get_token(self):
        url = self.url_base + "/api/aaaLogin.json"
        payload = {
            "aaaUser": {
                "attributes": {
                    "name": self.admin_name,
                    "pwd": self.password
                }
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        requests.packages.urllib3.disable_warnings()
        try:
            response = requests.post(url, data=json.dumps(
                payload), headers=headers, verify=False).json()
        except requests.exceptions.ConnectionError as c:
            print(c)
            logger.error("Connection Failed: " + str(c))
            exit()
        except BaseException as e:
            print(e)
            print('type is:', e.__class__.__name__)
            logger.error("Unhandled Exception: " + str(e))
            exit()

        if (response['imdata'][0]['aaaLogin']['attributes']['token']):
            return(response['imdata'][0]['aaaLogin']['attributes']['token'])
        else:
            logger.error("Unable to log: " + response["imdata"]
                         [0]["error"]["attributes"]["text"])
            exit()

# Funcion generica para crear objetos de cualquier tipo, depende del payload pasado
    def create_object(self, payload):
        url = self.url_base + "/api/mo/uni.json"
        headers = {
            "Cookie": f"APIC-Cookie={self._token}",
        }
        requests.packages.urllib3.disable_warnings()
        # En las plantillas hay que poner none como default en vez de "", se corrige aqui
        payload = self._dict_replace_value(payload, "none", "")
        payload = self._dict_replace_value(payload, "nan", "")
        print(payload)
        print("****************************************")
        response = requests.post(url, data=json.dumps(
            payload), headers=headers, verify=False)
        if (response.status_code == 200):
            if "name" in payload[list(payload.keys())[0]]["attributes"]:
                print("Successfully created " +
                      payload[list(payload.keys())[0]]["attributes"]["name"])
                logger.info("Successfully created " +
                            payload[list(payload.keys())[0]]["attributes"]["name"])
            else:
                print("Successfully associated: " +
                      payload[list(payload.keys())[0]]["attributes"]["dn"])
                logger.info("Successfully associated: " +
                            payload[list(payload.keys())[0]]["attributes"]["dn"])
        else:
            print("Issue with creating: " + str(response.status_code))
            print(json.loads(response.text)["imdata"]
                  [0]["error"]["attributes"]["text"])
            logger.error("Issue with creating: " + json.loads(response.text)["imdata"]
                         [0]["error"]["attributes"]["text"])

# Dos funcionaes para reemplazar none por "" en diccionarios anidados
    def _dict_replace_value(self, d, old, new):
        x = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = self._dict_replace_value(v, old, new)
            elif isinstance(v, list):
                v = self._list_replace_value(v, old, new)
            elif isinstance(v, str):
                v = v.replace(old, new)
            x[k] = v
        return x

    def _list_replace_value(self, l, old, new):
        x = []
        for e in l:
            if isinstance(e, list):
                e = self._list_replace_value(e, old, new)
            elif isinstance(e, dict):
                e = self._dict_replace_value(e, old, new)
            elif isinstance(e, str):
                e = e.replace(old, new)
            x.append(e)
        return x


def parse_data_excel(excel_file='data/datos_maestro.xlsx', templates_dir='templates/', save=False):
    all_dicts = {}
    for filename_full in os.listdir(templates_dir):
        if filename_full.endswith(".j2"):
            filename = filename_full[:-3]
            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template(templates_dir + filename_full)

            nodes = pd.read_excel(
                excel_file, sheet_name=filename, engine='openpyxl', na_values="null")
            nodes = nodes.where((pd.notnull(nodes)), None)
            nodes = nodes.to_dict(orient='records')
            # Al leer, el diccionario devuelve nan con valores no rellenos
            # Se eliminan para no tener que tratarlos mas adelante, si no estan, no estan
            nodes_2 = []
            for item in nodes:
                item_2 = {}
                for key, value in item.items():
                    if (str(value) != "nan" and str(value) != "None"):
                        item_2[key] = item[key]
                nodes_2.append(item_2)
            nodes = nodes_2
            print(nodes_2)
            if nodes != []:
                nodes_aux = []
                for item in nodes:
                    nodes_aux.append(validate_dict(filename, item))
                nodes = nodes_aux
                print(nodes)
            if save:
                with open("outputs/" + filename + ".yaml", "w") as w:
                    output = template.render(dataread=nodes)
                    w.write(output)
                w.close()


            # Versiones de pyaml anteriores a 6.0
            # all_dicts.update(yaml.load(template.render(dataread=nodes)))
            # Versiones de pyaml 6.0 y posteriores
            all_dicts.update(yaml.safe_load(template.render(dataread=nodes)))

    return all_dicts


if __name__ == '__main__':
    print("Estas ejecutando directamente aci_utils ")
