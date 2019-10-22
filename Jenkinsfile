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
//                     sh "docker image prune -a -f"
//                     sh "docker pull owasp/zap2docker-stable"
//                     sh "sudo chmod +x zap-docker.sh"
                    sh "docker-compose -f ./docker/docker-compose-selenium-zap.yml up -d zap"
//                     sh "export ZAP_IP=\$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' zap)"

                 }
             }

             stage('build python tests and selenium'){
                environment{
                    ZAP_ID="""
                            sh(${docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' zap})
                            """
                    }
                steps{

                    script{
                        sh "docker-compose -f ./docker/docker-compose-selenium-remote.yml build python-tests"
                        sh "docker-compose -f ./docker/docker-compose-selenium-remote.yml up -d selenium-server python-tests"
                        sh "docker wait python-tests zap selenium-server"
                        sh "docker-compose -f ./docker/docker-compose-selenium-remote.yml down"

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
//     post {
//         always {
//             script{
//
//                     sh "docker cp python-tests:/selenium/logs_dir . || true"
//                     sh "docker cp python-tests:/junit . ||true"
//                     sh "tar -zcvf screenshots.tar.gz logs_dir || true"
//                     junit allowEmptyResults: true, testResults: "junit/*.xml"
//                     archiveArtifacts allowEmptyArchive: true, artifacts: '*.tar.gz'
//                     sh "cd selenium/docker && docker-compose -f docker-compose-selenium.yml down"
//                     deleteDir()
//             }
//
//         }
//
//         success {
//             script{
//             if(env.STAGING == "true"){
//                     slackMember = "#jenkins-tests"
//                  }
//             slackSend (channel: slackMember, color: '#36A64F', message: "Tests SUCCESS!!!!. link to the build ${env.BUILD_URL}")
//             // updateGitlabCommitStatus name: ' ', state: 'success'
//             // emailext attachLog: true, body: "Job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (${env.BUILD_URL}) success", recipientProviders: [developers()], subject: 'Pipeline success'
//             //step([$class: 'Mailer', notifyEveryUnstableBuild: true, recipients: emailextrecipients([[$class: 'CulpritsRecipientProvider'], [$class: 'RequesterRecipientProvider']])])
//                }
//         }
//
//         failure {
//             script{
//                 if(env.automation_branch == "master"){
//                     slackMember = "#devops"
//                     }
//                 if(env.STAGING == "true"){
//                     slackMember = "#jenkins-tests"
//                  }
//                 slackSend (channel: slackMember, color: '#36A64F', message: "Tests FAILD!!. link to the build ${env.BUILD_URL}")
//                 archiveArtifacts allowEmptyArchive: true, artifacts: '*.tar.gz'
//                 }
//             // updateGitlabCommitStatus name: ' ', state: 'failed'
//             // emailext attachLog: true, body: "Job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (${env.BUILD_URL}) failed", recipientProviders: [developers()], subject: 'Pipeline failed', to: 'ifriedland@ravtech.co.il'
//             // mail to: 'devops@ravtech.co.il', subject: 'Pipeline failed', body: "Job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (${env.BUILD_URL}) failed"
//
//         }

//
//         unstable {
//             script{
//                 if(env.automation_branch == "master"){
//                     slackMember = "#devops"
//                     }
//                  if(env.STAGING == "true"){
//                     slackMember = "#jenkins-tests"
//                  }
//                 slackSend (channel: slackMember, color: '#36A64F', message: "Tests UNSTABLE!!. link to the build ${env.BUILD_URL}")
//                 }
//             // updateGitlabCommitStatus name: ' ', state: 'success'
//             // emailext attachLog: true, body: "Job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (${env.BUILD_URL}) unstable", recipientProviders: [developers()], subject: 'Pipeline unstable'
//         }
//
//     }


}
