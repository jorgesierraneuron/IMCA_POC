from tavily import TavilyClient
from concurrent.futures import ThreadPoolExecutor, as_completed


class Search:

    client = TavilyClient("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")
    queries = [
        "licitaciones públicas infraestructura República Dominicana site:listindiario.com after:2024",
        "proyectos de construcción relevantes República Dominicana site:.do after:2024",
        "inversiones extranjeras en infraestructura República Dominicana site:.do after:2024",
        "renovación urbana y zonas industriales República Dominicana site:.do after:2024",
        "compras públicas de maquinaria empresas constructoras República Dominicana site:.do after:2024"
    ]
    
    def __init__(self):
        pass 

    def __search_query(self,query, time_range: str, max_result: int):
        try:
            response = self.client.search(
                query=query,
                time_range=time_range,
                max_results=max_result,
                include_raw_content=True
            )

            response = [{"title": result["title"], "content": result["content"], "url":result["url"], "raw_content": result["raw_content"]} for result in response["results"]]

            
            return response 
        except Exception as e:
            return f"Error: {e}"
    
    def run(self, time_range: str, max_result: int):

        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_query = {executor.submit(self.__search_query, query, time_range, max_result): query for query in self.queries}
            for future in as_completed(future_to_query):
                result = future.result()
                results.append(result)
            
                
        
        result_plain = [d for item in results for d in item]

        

        vistos = set()
        result_plain_without_duplicates = []

        for item in result_plain:
            if item['title'] not in vistos:
                vistos.add(item['title'])
                result_plain_without_duplicates.append(item)

        return result_plain_without_duplicates




        

