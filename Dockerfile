FROM leo999/streamlit:v1
WORKDIR /root
RUN pip install pymysql
RUN rm -rf streamlit
RUN mkdir streamlit
COPY . streamlit
EXPOSE 8000

CMD ["/bin/bash"]
