pipeline {
    agent any
    stages {
        stage('Enable virtual environment pyats') {
            echo 'Setup PYATS environment'
            steps {
                sh 'python3 -m venv pyats'
                sh 'source pyats/bin/activate'
            }
        }
        stage('List Files in Directory') {
            echo 'Confirm the files are existing'
            steps {
                sh 'ls -la'
            }
        }        
        stage('Run the Python script apac_high_memory.py') {
            echo 'Activate Python script to check used memory'
            steps {
                sh 'python3 apac_high_memory.py --testbed apac_tb.yaml'
            }
        }
        stage('Copy output to Jenkins server directory') {
            echo 'Send output to FTP server'
            steps {
                sh '''
                ftp -inv 10.133.10.115 <<EOF
                user apacftp P@ssw0rd
                put apac_switch_memory.txt /apac_switch_memory.txt
                bye
                EOF
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
