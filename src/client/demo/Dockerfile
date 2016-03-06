FROM 20.26.17.136:5000/tomcat

# Maintainer: docker_user <docker_user at email.com> (@docker_user)
#MAINTAINER docker_user docker_user@email.com
#ENV JAVA_HOME=/home/jdk1.7.0_79
#ENV JAVA_BIN=/home/jdk1.7.0_79/bin
#ENV PATH=$PATH:$JAVA_BIN
#ENV CLASSPATH=$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
# Commands to update the image
copy *.war /usr/local/tomcat/webapps/
# Commands when creating a new container
#CMD /home/apache-tomcat-6.0.44/bin/catalina.sh run
