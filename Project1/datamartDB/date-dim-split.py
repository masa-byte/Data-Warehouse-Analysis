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
    session.read(flowFile, PyInputStreamCallback())
    flowfile_json = loadedJsonObject

    SALES_DATE = flowfile_json["SALES_DATE"]
    # sales date will be in format yyyy-mm-dd
    sales_date_split = SALES_DATE.split("-")
    SALES_YEAR = sales_date_split[0]
    SALES_MONTH = sales_date_split[1]
    SALES_DAY = sales_date_split[2]
    SALES_QUARTER = str((int(SALES_MONTH) - 1) // 3 + 1)

    attrMap = {
        "SALES_DATE": SALES_DATE,
        "SALES_YEAR": SALES_YEAR,
        "SALES_MONTH": SALES_MONTH,
        "SALES_DAY": SALES_DAY,
        "SALES_QUARTER": SALES_QUARTER,
    }
    flowFile = session.putAllAttributes(flowFile, attrMap)
    session.transfer(flowFile, REL_SUCCESS)
