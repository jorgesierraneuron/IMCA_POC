from openai import OpenAI
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed



@dataclass
class CompanyInfo:
    name: str
    description: str


class LLamager:

    def __init__(self, companyInfo: CompanyInfo, model: str):
       import os
       self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
       self.company_info = companyInfo
       self.model = model 
       self.model_evaluator = "o4-mini-2025-04-16"


    def __run_llm_evaluator(self,value_to_analyze: dict):
        
        
         

        instruction = f"""
        Rol:
        Eres un evaluador estratégico de oportunidades para una empresa. Tu misión es analizar noticias y determinar, con criterio preciso, si representan una oportunidad comercial futura y concreta para la empresa, en función de sus servicios actuales y capacidades.

        🧠 Criterios de Evaluación
        Responde solo con True o False, evaluando la noticia bajo los siguientes principios:

        ✅ Responde True si:
        La noticia describe una iniciativa futura, en curso o recién anunciada, como:

        Procesos de licitación pública o convocatorias abiertas.

        Anuncios de inversiones próximas o proyectos por ejecutar.

        Creación de nuevos programas, alianzas estratégicas o contratos por adjudicar.

        Planes de expansión, transformación digital o implementación de nuevas soluciones.

        Al menos uno de los servicios actuales de la empresa puede aplicar directamente a la necesidad expresada en la noticia.

        La empresa tiene posibilidades reales de participar o aportar valor en la etapa futura mencionada.

        Ejemplo válido (True):

        "Ministerio de minas ha abierto un proceo de licitacion iternacional para modernizacion de minas en colombia" → True
        Porque la licitación está abierta, lo que representa una oportunidad concreta.

        ❌ Responde False si:
        La noticia describe acciones ya finalizadas, como:

        Inauguración de obras ya ejecutadas.

        Proyectos concluidos, sin continuidad o sin necesidad futura.

        Contratos ya adjudicados o cerrados.

        Es una noticia conmemorativa o informativa, sin implicación de acción futura.

        No existe una conexión clara entre la noticia y los servicios actuales de la empresa.

        La empresa no tendría forma real de participar o aportar valor.

        Ejemplo no válido (False):

        "Gobierno inauguró 71 obras en el primer trimestre de 2025" → False
        Porque las obras ya fueron ejecutadas y no hay nada por ofrecer.

        ⚠️ Reglas clave
        Ignora noticias pasadas o finalizadas. Solo analiza oportunidades futuras o en curso.

        No debes hacer suposiciones. Basa tu juicio en lo que está explícitamente en la noticia.

        No expliques tu respuesta. No incluyas texto adicional.

        ✅ Tu tarea:
        Lee la noticia y responde estrictamente con uno de los siguientes valores:

        True → Si representa una oportunidad futura real, alineada con los servicios de la empresa.

        False → Si no hay oportunidad futura o no hay relación directa con los servicios. Tambien si no corresponde a una noticia
        
        Información de la empresa:

        Nombre: {self.company_info.name}
        Servicios y descripcion: 

        {self.company_info.description}
        """

        evaluate_new= f"""
        
        Noticia a evaluar: 
        
        Titulo: {value_to_analyze["title"]}
        Resumen: {value_to_analyze["content"]}
        Contenido: {value_to_analyze["raw_content"]}
        
        """

        
        response = self.client.responses.create(
                    model=self.model,
                    instructions=instruction,
                    input=evaluate_new,
                    )
        
        value_to_analyze["opportunity"] = response.output_text


        check = f"""
        Titulo: {value_to_analyze["title"]}
        check: {value_to_analyze["opportunity"]}
        check_directo: {response.output_text}
        """

        print(check)

        return value_to_analyze
    
    def __opportunity_evaluation(self,value_to_analyze: dict):

        instruction = f"""
        Rol:
        Eres un analista estratégico especializado en detectar oportunidades de negocio a partir de noticias relevantes. Tu función es identificar cómo una empresa puede capitalizar dichas noticias, alineando sus servicios actuales con las necesidades emergentes del mercado.

        🧠 Instrucciones Generales:
        Analiza la noticia: Examina cuidadosamente el contenido para identificar eventos clave, tendencias, necesidades del mercado, políticas gubernamentales, inversiones anunciadas o cambios regulatorios.

        Evalúa desde la perspectiva de la empresa: Considera siempre los servicios actuales de la empresa, su sector, capacidades y clientes objetivo.

        📝 Formato de Respuesta (Markdown)
        📌 Oportunidad Detectada
        Describe qué aspecto de la noticia representa una oportunidad.

        Explica por qué es relevante para la empresa (ej. alineación con servicios, nuevas necesidades del mercado, cambios regulatorios, etc.).

        🧩 Servicios Recomendados
        Enumera los servicios específicos que ofrece la empresa y que podrían aplicarse.

        Relaciona brevemente cada servicio con la oportunidad detectada.

        🚀 Acciones Estratégicas
        Lista acciones concretas para capitalizar la oportunidad (ej. contactar entidad, crear propuesta, lanzar piloto, adaptar servicio, etc.).

        Considera alianzas, diferenciadores o recursos clave que la empresa debe aprovechar.

        🏛️ Entidad o Cliente Potencial
        Identifica si hay una empresa, institución pública o privada, o entidad gubernamental involucrada o mencionada en la noticia que pueda ser un potencial cliente.

        Menciona su rol y por qué podría requerir los servicios de la empresa.

        🧭 Estilo y Tono:
        Respuesta concisa, directa y accionable.

        Usa listas con viñetas o numeradas.

        Usa negritas para destacar conceptos clave.

        Evita párrafos largos o explicaciones extensas.
        Nombre: {self.company_info.name}
        Servicios y descripcion: 

        {self.company_info.description}
        """

        evaluate_new= f"""
        Titulo: {value_to_analyze["title"]}
        Resumen: {value_to_analyze["content"]}
        Noticia: {value_to_analyze["raw_content"]}
        """

        
        response = self.client.responses.create(
                    model=self.model_evaluator,
                    instructions=instruction,
                    input=evaluate_new,
                    )
        
        value_to_analyze.pop("raw_content")
        value_to_analyze["recomendations"] = response.output_text

        return value_to_analyze


    

    def analyze(self, news_list):
        
        # for i in range(0, len(news_list), 5):
        #     news_sublist = news_list[i:i+5]
        final_result = []
        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_query = {executor.submit(self.__run_llm_evaluator, value): value for value in news_list}
            for future in as_completed(future_to_query):
                result = future.result()
                results.append(result)
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_query = {executor.submit(self.__opportunity_evaluation, value): value for value in news_list if value["opportunity"]== "True"}
            for future in as_completed(future_to_query):
                result = future.result()
                final_result.append(result)
        

        
        return final_result
        


            


