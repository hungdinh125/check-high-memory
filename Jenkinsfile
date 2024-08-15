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
                sh 'python3 check-high-memory/apac_high_memory.py --testbed check-high-memory/apac_tb.yaml'
            }
        }
        stage('Copy output to Jenkins server directory') {
            steps {
                sh 'sshpass -p 'P@ssw0rd' scp check-high-memory/apac_switch_memory.txt apacftp@10.133.10.115:/apac_switch_memory.txt'
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
