#!/usr/bin/env

from pydantic import BaseModel, validator, constr, conint
from ipaddress import IPv4Address
from typing import Optional, Type, Literal
from pydantic import BaseModel as PydanticBaseModel
import re

# Extendemos la clase BaseModel por defecto con nuestra propia clase para hacer strip por defecto


class BaseModel(PydanticBaseModel):
    class Config:
        anystr_strip_whitespace = True

# Cada clase tiene las variables de su template, con los validadores necesarios
# Para validadores mas complejos, se puede añadir una funcion


class Aps_dict_model(BaseModel):
    """Clase para validar el formato del diccionario aps_dict"""
    name: constr(strict=True, regex=r'^aps-\S+$')
    lip: constr(strict=True, regex=r'^lip-\S+$')
    lpg: constr(strict=True, regex=r'^lpg-\S+$')
    from_port: conint(strict=True, gt=0, lt=56)
    to_port: conint(strict=True, gt=0, lt=56)
    description: Optional[str] = None

    @validator('to_port')
    def to_port_check(cls, to_port, values):
        if values['from_port'] > to_port:
            raise ValueError(
                "to_port tiene que ser un numero menor que from_port")
        else:
            return to_port


class Bd_dict_model(BaseModel):
    """Clase para validar el formato del diccionario tnt_dict"""
    bd: constr(strict=True, regex=r'^bd-\S+$')
    tenant: constr(strict=True, regex=r'^tnt-\S+$')
    vrf: constr(strict=True, regex=r'^vrf-\S+$')
    description: Optional[constr(max_length=70)]
    bd_alias: Optional[constr(strict=True, regex=r'^vlan-\d{1,4}$')] = None
    arp_flooding: Optional[Literal['yes', 'no']]
    enable_routing: Optional[Literal['yes', 'no']] = None
    l2_unknown_unicast: Optional[Literal['flood', 'proxy']] = None
    multi_dest: Optional[Literal['bd-flood', 'drop', 'encap-flood']] = None
    erp: Optional[constr(strict=True, regex=r'^erp-\S+$')] = None
    gateway: Optional[IPv4Address] = None
    mask: Optional[constr(strict=True)] = None
    scope: Optional[Literal['private', 'public', 'shared']] = None
    l3out: Optional[constr(strict=True, regex=r'^l30-\S+$')] = None

    @validator('bd_alias')
    def vlan_check(cls, bd_alias):
        vlan = re.search('(\d+)$', bd_alias)
        if int(vlan.group(1)) > 4096:
            raise ValueError("El valor de la vlan no puede ser mayor de 4096")
        else:
            return bd_alias

    #Hay que forzar a que lo devuelva como string, sino devuelve un objeto tipo IPv4Address
    @validator('gateway')
    def return_gateway(cls,gateway):
        return(str(gateway))

    #Funcion brujeria de internet, ni he intentado entenderla, pero he probado y funciona
    #https://codereview.stackexchange.com/questions/209243/verify-a-subnet-mask-for-validity-in-python
    @validator('mask')
    def mask_check(cls,mask):
        a, b, c, d = (int(octet) for octet in mask.split("."))
        mask_tmp = a << 24 | b << 16 | c << 8 | d
        if mask_tmp == 0:
            raise ValueError("0.0.0.0 no se acepta como mascara", mask)
        m = mask_tmp & -mask_tmp
        right0bits = -1
        while m:
            m >>=1
            right0bits +=1
        if mask_tmp | ((1 << right0bits) - 1) != 0xffffffff:
            raise ValueError(mask + " no es una mascara de red correcta")
        else:
            #return 32 - right0bits #devolveriamos la mascara como numero
            return mask


class Epg_dict_model(BaseModel):
    """Clase para validar el formato del diccionario tnt_dict"""
    epg: constr(strict=True, regex=r'^epg-\S+$')
    tenant: constr(strict=True, regex=r'^tnt-\S+$')
    apf: constr(strict=True, regex=r'^apf-\S+$')
    bd: constr(strict=True, regex=r'^bd-\S+$')
    floodOnEncap: Optional[Literal['disabled', 'enabled']] = None
    description: Optional[constr(max_length=70)]
    epg_alias: Optional[constr(strict=True, regex=r'^vlan-\d{1,4}$')] = None
    

    @validator('epg_alias')
    def vlan_check(cls, epg_alias):
        vlan = re.search('(\d+)$', epg_alias)
        if int(vlan.group(1)) > 4096:
            raise ValueError("El valor de la vlan no puede ser mayor de 4096")
        else:
            return epg_alias

class Tnt_dict_model(BaseModel):
    """Clase para validar el formato del diccionario tnt_dict"""
    tenant: constr(strict=True, regex=r'^tnt-\S+$')
    description: Optional[constr(strict=True)] = None


def validate_dict(dict_type, my_dict):
    """Clase para validar un diccionario, tiene que recibir el tipo de diccionario"""
    validated_obj = None
    if dict_type == 'aps':
        validated_obj = Aps_dict_model(**my_dict)
    elif dict_type == 'bd':
        validated_obj = Bd_dict_model(**my_dict)
    elif dict_type == 'epg':
        validated_obj = Epg_dict_model(**my_dict)
    elif dict_type == 'tnt':
        validated_obj = Tnt_dict_model(**my_dict)
    try:
        # Al crear las clases con atributos, el diccionario devuelve nan con valores no rellenos
        # Se eliminan para no tener que tratarlos mas adelante, si no estan, no estan
        for key, value in list(validated_obj.__dict__.items()):
            if value == None:
                validated_obj.__dict__.pop(key)
        return validated_obj.__dict__
    except AttributeError:
        raise Exception("No se ha encontrado el tipo de diccionario")
    del validated_obj


if __name__ == '__main__':
    print("Estas ejecutando directamente validator_mode_utils ")
