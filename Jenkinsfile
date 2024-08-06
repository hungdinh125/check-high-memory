pipeline {
    agent any
    stages {
        stage('Build Docker container') {
            steps {
                echo 'Build container'
                sh "docker run -dit --name ansible_git netdevops/ansible_git_v1"
            }
        }
     
        stage('Clone the repository to container') {
            steps {
                sh 'docker exec -i ansible_git /bin/sh -c "git clone https://github.com/hungdinh125/check-high-memory.git"'                
            }
        }

        stage('Install pyats, genie and scp') {
            steps {
                sh 'docker exec -i ansible_git /bin/sh -c "pip3 install pyats"'
                sh 'docker exec -i ansible_git /bin/sh -c "pip3 install genie"'
                sh 'docker exec -i ansible_git /bin/sh -c "sudo yum install -y openssh-clients'
            }
        }
                
        stage('Run the Python script apac_high_memory.py') {
            steps {
                sh 'docker exec -i ansible_git /bin/sh -c "python3 check-high-memory/apac_high_memory.py --testbed check-high-memory/apac_tb.yaml"'
            }
        }
        stage('Copy output to Jenkins server directory') {
            steps {
                sh 'docker exec -i ansible_git /bin/sh -c "cp check-high-memory/apac_switch_memory.txt ."'
                sh 'docker exec -i ansible_git /bin/sh -c "scp check-high-memory/apac_switch_memory.txt network:network@10.127.10.29/apac_switch_memory.txt"'
            }
        }
    }
    post {
        always {
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true)
            sh "docker rm -f ansible_git"
        }
    }
}
