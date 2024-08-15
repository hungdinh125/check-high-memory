pipeline {
    agent any
    stages {
        stage('Enable virtual environment pyats') {
            steps {
                echo 'Setup PYATS environment'
                sh 'python3 -m venv pyats'
                sh 'source pyats/bin/activate'
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
