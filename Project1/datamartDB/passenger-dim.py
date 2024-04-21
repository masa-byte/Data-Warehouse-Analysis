from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import InputStreamCallback
import json
from java.lang import Object
from jarray import array


class PyInputStreamCallback(InputStreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream):
        global loadedJsonObject
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        loadedJsonObject = json.loads(text)


flowFile = session.get()
if flowFile != None:
    PASSENGER_ID = flowFile.getAttribute("PASSENGER_ID")
    NAME = flowFile.getAttribute("NAME")
    SURNAME = flowFile.getAttribute("SURNAME")
    AGE = flowFile.getAttribute("AGE")
    CLASS = flowFile.getAttribute("CLASS")
    COUNTRY = flowFile.getAttribute("COUNTRY")
    GENDER = flowFile.getAttribute("GENDER")

    session.read(flowFile, PyInputStreamCallback())
    flowfile_json = loadedJsonObject
    passenger_exists = "no"
    for_update = "yes"

    PASSENGER_DIM_ID = ""
    if "PASSENGER_DIM_ID" in flowfile_json:
        passenger_exists = "yes"

        PASSENGER_DIM_ID = flowfile_json["PASSENGER_DIM_ID"]
        PASSENGER_ID_R = flowfile_json["PASSENGER_ID"]
        NAME_R = flowfile_json["PASSENGER_NAME"]
        SURNAME_R = flowfile_json["PASSENGER_SURNAME"]
        AGE_R = flowfile_json["PASSENGER_AGE"]
        CLASS_R = flowfile_json["PASSENGER_CLASS"]
        COUNTRY_R = flowfile_json["PASSENGER_COUNTRY"]
        GENDER_R = flowfile_json["PASSENGER_GENDER"]

        if (
            PASSENGER_ID_R == PASSENGER_ID
            and NAME_R == NAME
            and SURNAME_R == SURNAME
            and AGE_R == AGE
            and CLASS_R == CLASS
            and COUNTRY_R == COUNTRY
            and GENDER_R == GENDER
        ):

            for_update = "no"

    attrMap = {
        "passenger_exists": passenger_exists,
        "for_update": for_update,
        "PASSENGER_DIM_ID": PASSENGER_DIM_ID,
    }
    flowFile = session.putAllAttributes(flowFile, attrMap)
    session.transfer(flowFile, REL_SUCCESS)
