from cfdi.classes import XmlNewObject
xml = """<?xml version="1.0" encoding="UTF-8"?>
    <cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/3" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    Certificado="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" Fecha="2020-07-29T13:13:02" Folio="1902" FormaPago="99" LugarExpedicion="78049" MetodoPago="PPD" Moneda="MXN" NoCertificado="00001000000404293544" Sello="hZdGiUH8I1rowHa5M2hhtribsre0TjwF5mxIn21wQEmLznSoY+xtSmg1+xtcQTddQmq/BkYaBRtvzeT56umzhB2gSVsH9CdK0p4bXHtVaTBcgVKDLFJc21WKfJkmTLP8NQNLYQrCwKmWUewm/T5CJ5I2Ry7ei7af/IJaksBhcvaS0/ol6v1EDYutX2j1vziR+LHtvmv5u/25mIB6uSq39JIqaca5SHu/y39BGXTradwxorOfRUUlAb0VTV1RWr00nZdXJJydBFKrz+9ZL9fYfRvJ1zWLc67TrGo9fGAarV65vxUzm/6MiMjaCfoauZaQbm01CjHTPo3d/+taBSmmjg==" Serie="F" SubTotal="667.83" TipoDeComprobante="I" Total="774.68" Version="3.3" xsi:schemaLocation="http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd"><cfdi:Emisor Nombre="Roberto Aceves Alvarado" RegimenFiscal="612" Rfc="AEAR791212MM3"/><cfdi:Receptor Nombre="VICTOR MANUEL ESCAMILLA TINAJERO" Rfc="EATV530415SW9" UsoCFDI="P01"/><cfdi:Conceptos><cfdi:Concepto Cantidad="1.0000" ClaveProdServ="12141903" ClaveUnidad="A75" Descripcion="NITROGENO GASEOSO INDUSTRIAL INF 9MTS C.103090" Importe="667.8324" NoIdentificacion="NGII9C" Unidad="CARGA" ValorUnitario="667.8324"><cfdi:Impuestos><cfdi:Traslados><cfdi:Traslado Base="667.8324" Importe="106.8532" Impuesto="002" TasaOCuota="0.160000" TipoFactor="Tasa"/></cfdi:Traslados></cfdi:Impuestos></cfdi:Concepto></cfdi:Conceptos><cfdi:Impuestos TotalImpuestosTrasladados="106.85"><cfdi:Traslados><cfdi:Traslado Importe="106.85" Impuesto="002" TasaOCuota="0.160000" TipoFactor="Tasa"/></cfdi:Traslados></cfdi:Impuestos>
    
    <cfdi:Complemento>
    <tfd:TimbreFiscalDigital FechaTimbrado="2020-07-29T13:13:05" 
    NoCertificadoSAT="00001000000504204971" RfcProvCertif="PPD101129EA3" SelloCFD="hZdGiUH8I1rowHa5M2hhtribsre0TjwF5mxIn21wQEmLznSoY+xtSmg1+xtcQTddQmq/BkYaBRtvzeT56umzhB2gSVsH9CdK0p4bXHtVaTBcgVKDLFJc21WKfJkmTLP8NQNLYQrCwKmWUewm/T5CJ5I2Ry7ei7af/IJaksBhcvaS0/ol6v1EDYutX2j1vziR+LHtvmv5u/25mIB6uSq39JIqaca5SHu/y39BGXTradwxorOfRUUlAb0VTV1RWr00nZdXJJydBFKrz+9ZL9fYfRvJ1zWLc67TrGo9fGAarV65vxUzm/6MiMjaCfoauZaQbm01CjHTPo3d/+taBSmmjg==" SelloSAT="wvokkitNLw+nMOdESLojJXTUW9LtkVcaXdVmq6Bw8Uf2KJt7gDvBtCkfeKCn9hbhYaRW6uKDMC+NeOr4TyJAEdC4JZn/MWEFfk/z07kPT2lx9ebch29J5i7F7GknKFHmHqkwnxi7XoSzKpWIJamPU8Md0yZOqCbc+LLuU6/LD8sHTGp6PS39mkEZSMWXTvVHLnfe4IuliX9D7o1DX+GTZCI9vd1v+I5PlPa2ot1GbS3yyo+Mdv31gou5DsNpCFdDoamlDPfJliXRDYgBsJjsaxsoU+N9MIcBavAMXwsXR2UZDOLnUA0XTnRCX2wPv529TbN/Y/ldko/J4KRwuTIsgw==" UUID="284DE08B-AE18-4363-B898-E28CA88B05C0" Version="1.1" 
    xsi:schemaLocation="http://www.sat.gob.mx/TimbreFiscalDigital http://www.sat.gob.mx/sitio_internet/cfd/timbrefiscaldigital/TimbreFiscalDigitalv11.xsd" xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital"/>
    </cfdi:Complemento></cfdi:Comprobante>"""

_(
    XmlNewObject(xml).validar_cfdi()
)