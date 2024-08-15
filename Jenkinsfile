pipeline {
    agent any
    stages {
        stage('Enable virtual environment pyats') {
            steps {
                sh 'python3 -m venv pyats'
                sh 'source pyats/bin/activate'
            }
        }
        stage('Clone the repository to container') {
            steps {
                sh 'git clone https://github.com/hungdinh125/check-high-memory.git'                
            }
        }        
        stage('Run the Python script apac_high_memory.py') {
            steps {
                sh 'python3 apac_high_memory.py --testbed apac_tb.yaml'
            }
        }
        stage('Debug: List Files in Directory') {
            steps {
                sh 'ls -la'
                sh 'ls -l check-high-memory/'
            }
        }
        stage('Copy output to Jenkins server directory') {
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
