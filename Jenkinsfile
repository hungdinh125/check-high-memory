pipeline {
    agent any
    stages {
        stage('Enable virtual environment pyats') {
            steps {
                echo 'Setup PYATS environment'
                sh '''
                python3 -m venv pyats'
                source pyats/bin/activate
                '''
            }
        }
        stage('List Files in Directory') {
            steps {
                echo 'Confirm the files are existing'
                sh 'ls -la'
            }
        }        
        stage('Run the Python script apac_high_memory.py') {
            steps {
                echo 'Activate Python script to check used memory'
                sh 'python3 apac_high_memory.py --testbed apac_tb.yaml'
            }
        }
        stage('Copy output to Jenkins server directory') {
            steps {
                echo 'Send output to FTP server'
                sh '''
                ftp -inv 10.133.10.115 <<EOF
                user apacftp P@ssw0rd
                put apac_switch_memory.txt /apac_switch_memory.txt
                bye
                EOF
                '''
            }
        }
        stage('Output the result in console') {
            steps {
                echo 'Check the result in console interface'
                sh 'cat apac_switch_memory.txt'
            }
        }
        stage('Post to MS Teams') {
            steps {
                echo 'Display result to MS Teams channel'
                sh '''
                curl -H 'Content-Type: application/json' \
                     -d "{\"text\": \"$(cat apac_switch_memory.txt | sed 's/\"/\\"/g')\"}" \
                     https://aligntech.webhook.office.com/webhookb2/7ed9a6c7-e811-4e71-956c-9e54f8b7d705@9ac44c96-980a-481b-ae23-d8f56b82c605/JenkinsCI/9ecff2f044b44cfcae37b0376ecd1540/9d21b513-f4ee-4b3b-995c-7a422a087a6c
                '''
            }
        }
    }
    post {
        always {
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true)
        }
    }
}
