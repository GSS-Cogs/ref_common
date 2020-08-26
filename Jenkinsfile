@Library('pmd@family-pmd4') _

import uk.org.floop.jenkins_pmd.Drafter

pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('Test') {
            agent {
                docker {
                    image 'cloudfluff/csvlint'
                    reuseNode true
                    alwaysPull true
                }
            }
            steps {
                script {
                    ansiColor('xterm') {
                        sh "csvlint -s measures.csv-metadata.json"
                    }
                }
            }
        }
        stage('Add common/GSS components') {
            steps {
                script {
                    def pmd = pmdConfig('pmd')
                    for (myDraft in pmd.drafter
                            .listDraftsets(Drafter.Include.OWNED)
                            .findAll { it['display-name'] == env.JOB_NAME }) {
                        pmd.drafter.deleteDraftset(myDraft.id)
                    }
                    def id = pmd.drafter.createDraftset(env.JOB_NAME).id
                    for (graph in util.jobGraphs(pmd, id)) {
                        pmd.drafter.deleteGraph(id, graph)
                        echo "Removing own graph ${graph}"
                    }
                    sh "csv2rdf -t 'measures.csv' -u 'measures.csv-metadata.json' -m annotated -o measures.ttl"
                    writeFile file: "graph.sparql", text:  """SELECT ?graph { ?graph a <http://www.w3.org/2002/07/owl#Ontology> }"""
                    sh "sparql --data='measures.ttl' --query=graph.sparql --results=JSON > 'measures-graph.json'"
                    def graph = readJSON(text: readFile(file: "measure-graph.json")).results.bindings[0].graph.value
                    pmd.drafter.addData(
                            id,
                            "${WORKSPACE}/measures.ttl",
                            "text/turtle",
                            "UTF-8",
                            graph
                    )
                    writeFile(file: "measures-prov.ttl", text: util.jobPROV(graph))
                    pmd.drafter.addData(
                            id,
                            "${WORKSPACE}/measures-prov.ttl",
                            "text/turtle",
                            "UTF-8",
                            graph
                    )
                    pmd.drafter.publishDraftset(id)
                }
            }
        }
    }
}