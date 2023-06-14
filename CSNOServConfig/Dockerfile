FROM tomcat:8.5.89-jdk8-corretto-al2
RUN groupadd -g 1000 ec2-user && \    
    useradd -u 1000 -g ec2-user -m ec2-user -G docker_env && \   
    usermod -p "*" ec2-user
COPY csnoserv.war /usr/local/tomcat/webapps/
EXPOSE 8080
CMD ["catalina.sh", "run"]