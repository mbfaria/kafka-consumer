# Kafka, Spark Streaming, Schema Registry, e Execução de Códigos Scala em PySpark

Este projeto é um estudo que combina diversas tecnologias para criar um ambiente de processamento de streaming de dados com Kafka, Spark Streaming, Schema Registry e a execução de códigos Scala dentro do PySpark. Ele demonstra como consumir, processar e analisar dados em tempo real de maneira eficiente.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
.
├── README.md
├── check_messages.sh
├── docker-compose.yml
├── requirements.txt
├── scala-code
│   ├── README.md
│   ├── build.sbt
│   ├── project
│   │   └── build.properties
│   ├── src
│   │   ├── main
│   │   │   └── scala
│   │   │       └── Main.scala
│   │   └── test
│   │       └── scala
│   │           └── MySuite.scala
│   └── target
│
└── src
    ├── event_consumer.py
    └── event_producer.py
```

- **README.md**: O arquivo que você está lendo agora, fornecendo uma visão geral do projeto.

- **check_messages.sh**: Um script para visualizar mensagens no tópico do Kafka usado para depuração.

- **docker-compose.yml**: Configuração do ambiente Docker com Kafka e Schema Registry.

- **requirements.txt**: Lista de bibliotecas Python necessárias para o projeto.

- **scala-code**: Diretório contendo o código Scala e a estrutura de compilação associada.

- **src**: Diretório com os scripts Python para produção e consumo de eventos.

## Sobre o Projeto

O diretório `scala-code` contém o código Scala necessário para o projeto, incluindo as configurações de compilação e testes. É usado para executar código Scala no ambiente PySpark.

O diretório `src` contém os seguintes arquivos Python:

- **event_producer.py**: Um script que gera eventos e os envia para o Kafka, incluindo a definição do esquema no formato Avro e registro no Schema Registry.

- **event_consumer.py**: Um consumidor de eventos que utiliza Spark Streaming para consumir os dados do Kafka, deserializá-los com base no esquema presente no Schema Registry e executar um código Scala no ambiente PySpark.

## Configuração do Ambiente

Para recriar o ambiente, siga estas etapas:

1. Crie um ambiente virtual Python:

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instale as bibliotecas necessárias:

   ```
   pip install -r requirements.txt
   ```

3. Inicie o ambiente Docker usando o arquivo `docker-compose.yml`:

   ```
   docker-compose up
   ```

## Executando o Projeto

1. Execute o script `event_producer.py` para enviar eventos ao Kafka com esquema Avro registrado no Schema Registry.

2. Para fins de depuração, você pode usar o script `check_messages.sh` para visualizar mensagens no tópico do Kafka.

3. Execute o script `event_consumer.py` para consumir, deserializar e processar os eventos usando Spark Streaming e PySpark.


## Compilando e Adicionando Código Scala em PySpark

Para incorporar o código Scala em seu ambiente PySpark, siga as etapas abaixo:

### 1. Instalando o SBT (Scala Build Tool)

Antes de compilar o código Scala, você precisa ter o SBT instalado. Siga as instruções no [site oficial do SBT](https://www.scala-sbt.org/download.html) para instalar o SBT em seu sistema.

### 2. Estrutura do Diretório Scala

Certifique-se de que seu diretório `scala-code` está organizado da seguinte maneira:

```
scala-code
├── README.md
├── build.sbt
├── project
│   └── build.properties
├── src
│   ├── main
│   │   └── scala
│   │       └── Main.scala
├── target
```

Para fazer isso sugiro utilizar o commando `sbt new scala/scala3.g8` para criar um projeto em Scala 3. Quando aparecer no prompt para nomear a aplicação digite `scala-code` ou o nome que preferir.

### 3. Configurando o arquivo `build.sbt`

Dentro do diretório `scala-code`, você encontrará o arquivo `build.sbt`. Este arquivo é responsável pela configuração do projeto Scala e suas dependências. Abra-o em um editor de texto e certifique-se de que ele esteja configurado corretamente.

Exemplo de um `build.sbt` básico:

```scala
name := "MeuProjetoScala"

version := "1.0"

scalaVersion := "2.12.10"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "2.4.8",
  "org.apache.spark" %% "spark-sql" % "2.4.8"
  // Adicione outras dependências conforme necessário
)
```

Aqui, estamos configurando um projeto Scala chamado "MeuProjetoScala" com a versão do Scala e as dependências do Spark.

### 4. Compilando o Código Scala

No diretório `scala-code`, abra um terminal e execute o seguinte comando para compilar o código Scala e criar um arquivo JAR:

```shell
sbt clean package
```

Este comando irá compilar seu projeto Scala e gerar um arquivo JAR na pasta `target/scala-2.12`.

### 5. Adicionando o Código Scala ao PySpark

Agora que você compilou seu código Scala, você pode adicionar o arquivo JAR gerado ao ambiente PySpark. Para fazer isso, você pode usar o seguinte comando:

```shell
pyspark --jars /caminho/para/scala-code/target/scala-2.12/MeuProjetoScala-1.0.jar
```

Substitua `/caminho/para/scala-code/target/scala-2.12/MeuProjetoScala-1.0.jar` pelo caminho real para o arquivo JAR gerado pelo SBT.

Ou você pode adicionar manualmente dentro do `spark.jars` no Spark Session: 
```python
spark = (
    SparkSession.builder.appName("MySession")
    .config(
        "spark.jars",
        "/caminho/para/scala-code/target/scala-2.12/MeuProjetoScala-1.0.jar",
    )
    .getOrCreate()
)
```

Agora você está pronto para executar código Scala dentro do ambiente PySpark, aproveitando as funcionalidades do Spark para processamento de dados em larga escala.

Lembre-se de adaptar essas instruções de acordo com a estrutura e configurações específicas do seu projeto Scala.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas ou solicitações de pull.
