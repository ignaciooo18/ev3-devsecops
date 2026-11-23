pipeline {
    agent any

    environment {
        APP_NAME = "securedev-app"
        CONTAINER_NAME = "flask-prod"
    }

    stages {
        stage('1. Construccion') {
            steps {
                echo 'Construyendo imagen Docker...'
                sh 'docker build -t ${APP_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('2. Revision SAST (Bandit)') {
            steps {
                echo 'Ejecutando analisis estatico de seguridad (SAST) con Bandit...'
                sh '''
                    docker rm -f bandit-temp || true
                    docker create --name bandit-temp python:3.11-slim bash -c "pip install -q bandit && bandit -r /tmp/app.py -f txt -o /tmp/bandit-report.txt || true"
                    docker cp app.py bandit-temp:/tmp/app.py
                    docker start -a bandit-temp
                    docker cp bandit-temp:/tmp/bandit-report.txt ./bandit-report.txt
                    docker rm -f bandit-temp
                    cat bandit-report.txt
                '''
            }
        }

        stage('3. Despliegue') {
            steps {
                echo 'Desplegando aplicacion en Docker...'
                sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${APP_NAME}:${BUILD_NUMBER}
                    sleep 5
                '''
            }
        }

        stage('4. Pruebas Seguridad OWASP ZAP') {
            steps {
                echo 'Ejecutando pruebas dinamicas DAST con OWASP ZAP...'
                sh '''
                    docker rm -f zap-temp || true
                    docker run --name zap-temp ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://host.docker.internal:5000/hello?name=test -r zap-report.html || true
                    docker cp zap-temp:/zap/wrk/zap-report.html ./zap-report.html
                    docker rm -f zap-temp || true
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'bandit-report.txt, zap-report.html', allowEmptyArchive: true
        }
    }
}