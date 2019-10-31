def AGENT_LABEL = null

node('master') {
  stage('Checkout and set agent'){
     checkout scm
     if (env.SLAVE) {
        AGENT_LABEL = env.SLAVE

     } else {
        AGENT_LABEL = "test-ravtech"
     }
     sh "echo ${AGENT_LABEL}"
   }
}

pipeline {
    agent { label "${AGENT_LABEL}" }
    stages {
        stage('Build zap env') {
             steps {
                 script{
                    sh "docker kill zap selenium-server python-tests || true"
                    sh "docker system prune -af"
                    sh "docker-compose -f ./docker/docker-compose-ci.yml up -d"
                    sh "docker logs python-tests"
                    sh "docker wait python-tests"
                    sh "docker-compose -f ./docker/docker-compose-ci.yml down"

                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: './zap_reports',
                        reportFiles: 'test.html',
                        reportName: 'ZAP  Report',
                        reportTitles: ''
                    ])
                 }
             }
        }
    }
}