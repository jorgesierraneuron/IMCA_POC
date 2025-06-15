from utils.tavily import Search
from utils.llamager import LLamager, CompanyInfo

name = "IMCA"
description = """
IMCA es una empresa dominicana con más de 78 años de experiencia, dedicada a servir a diversas industrias como construcción, minería, agroindustria, comercio y transporte.  Ofrecen una amplia gama de servicios para optimizar las operaciones de sus clientes, incluyendo:
Venta y alquiler de equipos: Proporcionan equipos nuevos y usados de marcas reconocidas como CAT®, John Deere, Metso Outotec, entre otras. 


Repuestos: Ofrecen una amplia gama de repuestos originales para las marcas que representan, disponibles para compra en línea y entrega a través de su servicio Delivery IMCA. 


Servicio técnico: Cuentan con técnicos especializados que realizan reparaciones rápidas y según las especificaciones del fabricante, garantizando la vida útil de los equipos. 


Planes de cobertura: Ofrecen protección adicional para equipos después del vencimiento de la garantía de fábrica, cubriendo posibles averías mecánicas. 


Acuerdos de mantenimiento: Brindan planes de mantenimiento preventivo para asegurar el óptimo funcionamiento de los equipos y prolongar su vida útil. 


Monitoreo de equipos: Ofrecen servicios de monitoreo en tiempo real para supervisar el rendimiento y detectar posibles fallas en los equipos, permitiendo una respuesta inmediata. 


Financiamiento: Proporcionan diversas opciones de financiamiento para la adquisición de equipos, repuestos o servicios, facilitando la compra y apoyando el crecimiento de los negocios de sus clientes
"""

model = "gpt-4.1-nano-2025-04-14"
company_info = CompanyInfo(name,description)
search = Search()
llamager = LLamager(company_info,model)

results = search.run("week", 1)

analyze_news = llamager.analyze(results)

print(analyze_news)