from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

class VideoUploadView(APIView):
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LLMSearchView(APIView):
    def post(self, request):
        query = request.data.get('query', '')
        
        # Initialize LLM (replace with your preferred model)
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_template(
            "Answer the following question about the uploaded video: {query}"
        )
        
        # Create search chain
        search_chain = prompt | llm | StrOutputParser()
        
        # Invoke the chain
        result = search_chain.invoke({"query": query})
        
        return Response({"answer": result})

