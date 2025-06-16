from openai import OpenAI
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import streamlit as st



@dataclass
class CompanyInfo:
    name: str
    description: str


class LLamager:

    def __init__(self, companyInfo: CompanyInfo, model: str, analyst: str):
       
       self.client = OpenAI(api_key=st.secrets["OPENAI_KEY"])
       self.company_info = companyInfo
       self.model = model 
       self.model_evaluator = "o4-mini-2025-04-16"
       self.analyst = analyst


    def __run_llm_evaluator(self, value_to_analyze: dict):
        
        if self.analyst == "estratega":
         

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

        if self.analyst == "riesgo":
            instruction = f"""
            Rol:
                Eres un **analista de riesgos externo** altamente especializado. Tu misión es monitorear y evaluar noticias de medios de comunicación para identificar **potenciales amenazas externas** que puedan afectar negativamente a la empresa objetivo.

            🧠 Criterios de Evaluación de Amenazas:

                Para cada noticia, tu tarea es determinar, con precisión y sin suposiciones, si representa una **amenaza externa real y concreta** para la empresa, en función de su contexto de operación y los riesgos que podría enfrentar.

                ✅ Responde True si TODOS los siguientes principios se cumplen:
                    1. La noticia describe un evento, situación o anuncio **reciente, en curso o inminente** que tiene el potencial de generar un impacto negativo.
                    2. El evento o situación descrito puede **afectar directamente** a la empresa en al menos una de las siguientes áreas:
                        * **Competencia:** Surgimiento de nuevos competidores, estrategias agresivas de precios, tecnologías disruptivas en el sector.
                        * **Regulatorio / Legal:** Cambios en leyes, normativas, impuestos o restricciones que impacten sus operaciones.
                        * **Licitaciones / Contrataciones:** Pérdida de concursos importantes, exclusiones, favoritismo hacia competidores.
                        * **Reputación / Imagen Pública:** Escándalos, mala prensa, controversias, o problemas de socios/proveedores que la asocien negativamente.
                        * **Condiciones del Mercado:** Inestabilidad económica, recesión, fluctuaciones de precios de materias primas, caída de la demanda.
                        * **Tecnología / Sustitución:** Aparición de nuevas tecnologías o soluciones que puedan reemplazar sus servicios o productos principales.
                        * **Eventos Externos (Fuerza Mayor):** Desastres naturales, huelgas, conflictos geopolíticos, interrupciones logísticas o de cadena de suministro.
                    3. El impacto potencial en la empresa es **significativo** (no es un evento menor sin consecuencias claras).

                ❌ Responde False si CUALQUIERA de los siguientes principios se cumple:
                    1. La noticia describe un evento o situación **pasada o ya mitigada** sin implicaciones futuras de riesgo.
                    2. La noticia es puramente **informativa o conmemorativa**, sin un vínculo claro con una amenaza directa para la empresa.
                    3. **No existe una conexión clara o directa** entre el contenido de la noticia y una amenaza para la empresa.
                    4. El impacto potencial en la empresa es **mínimo o insignificante**.
                    5. La noticia no corresponde a un hecho relevante o es irrelevante para el monitoreo de riesgos de la empresa.

            ⚠️ Reglas Clave:
                * Ignora noticias que no presenten un riesgo futuro o en curso.
                * No debes hacer suposiciones. Basa tu juicio **exclusivamente en lo que está explícitamente en la noticia** y la información proporcionada sobre la empresa.
                * **No expliques tu respuesta.** No incluyas texto adicional, justificaciones ni ejemplos.
                * Tu respuesta debe ser estrictamente `True` o `False`.

            ---

            Información de la empresa objetivo:
            Nombre: {self.company_info.name}
            Contexto de operación (servicios y descripción):
            {self.company_info.description}

            ---

            Noticia a evaluar:
            Título: {value_to_analyze["title"]}
            Resumen: {value_to_analyze["content"]}
            Contenido: {value_to_analyze["raw_content"]}

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

        st.code(check, language='text') 

        return value_to_analyze
    
    def __opportunity_evaluation(self, value_to_analyze: dict):

        
        if self.analyst=='estratega':
        
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

    

        if self.analyst=="riesgo":

            
            
            instruction = f"""
            Actúa como un analista de riesgos externo que monitorea medios de comunicación para identificar potenciales amenazas externas que puedan afectar negativamente a una empresa.

            La empresa objetivo es: {self.company_info.name}
            Su contexto de operación es:
            {self.company_info.description}

            Busca noticias recientes que puedan representar una amenaza y responde en el formato estructurado siguiente.
            Clasifica cada amenaza usando uno o más de los siguientes tags de categoría:

            🏷️ Competencia – Nuevos jugadores, ofertas agresivas, pérdida de mercado

            ⚖️ Regulatorio / Legal – Cambios en leyes, impuestos, normativas, restricciones

            🧾 Licitaciones / Contrataciones – Pérdida de concursos, exclusiones, favoritismo

            🧨 Reputación / Imagen Pública – Escándalos, mala prensa, socios comprometidos

            📉 Condiciones del Mercado – Inestabilidad, recesión, caída de inversión pública

            🔧 Tecnología / Sustitución – Aparición de soluciones que reemplazan sus servicios

            🌪️ Eventos Externos – Desastres naturales, huelgas, conflictos logísticos

            Para cada amenaza detectada, responde con el siguiente formato:

            📄 Formato de respuesta para cada amenaza
            🔹 Título de la noticia:
            [TÍTULO]

            🏷️ Categorías de amenaza (Tags):
            [Ej: “Competencia”, “Licitaciones / Contrataciones”]

            📄 Resumen:
            Breve descripción del hecho o noticia (máx. 3 líneas)

            📊 Relevancia para {self.company_info.name}:
            Alta / Media / Baja (según el impacto potencial en sus operaciones, reputación o mercado)

            🧠 Acciones Estratégicas recomendadas:
            Enumera entre 1 y 3 pasos o sugerencias concretas que podrían tomarse para mitigar el riesgo o anticiparse al problema (Ej: establecer contacto con entidad reguladora, revisar precios vs competencia, reforzar relación con cliente clave, etc.)

            ✅ Ejemplo de salida (IA generada)
            🔹 Título de la noticia:
            “Gobierno adjudica contrato millonario de asfaltado a nuevo consorcio brasileño”


            🏷️ Categorías de amenaza (Tags):
            “Competencia”, “Licitaciones / Contrataciones”

            📄 Resumen:
            Un nuevo consorcio extranjero ganó una licitación para asfaltado vial que históricamente era liderada por empresas locales con maquinaria Caterpillar.


            📊 Relevancia para IMCA:
            Alta

            🧠 Acciones Estratégicas recomendadas:

            Analizar condiciones de la licitación ganadora para detectar ventajas competitivas

            Identificar si el consorcio requiere proveedores de maquinaria o soporte local

            Evaluar si hay riesgo de pérdida de cuota de mercado en otros proyectos similares
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
        


            


