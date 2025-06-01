# TCC - Utilização de Redes Neurais Convolucionais para Detecção de EPIs | Use of Convolutional Neural Networks for PPE Detection

## 📌 Nota Técnica sobre este Projeto | Technical Note about this Project


### 🇧🇷 Português

Este projeto foi desenvolvido como parte do meu **Trabalho de Conclusão de Curso (TCC)** em Ciência da Computação pela FEMA - Fundação Educacional do Município de Assis. O trabalho propõe uma aplicação prática de **Visão Computacional** e **Inteligência Artificial** para promover a **segurança no ambiente de trabalho** por meio da detecção automática de **Equipamentos de Proteção Individual (EPIs)** utilizando o modelo **YOLOv8**.


**Motivação para manter este projeto ativo:**  
Ao contrário de projetos que preservo em estado original, este projeto segue como um exemplo representativo da minha capacidade atual de integrar **Machine Learning**, **desenvolvimento web** e **engenharia de software**. Optei por mantê-lo público e documentado como demonstração da minha competência técnica e capacidade de conduzir projetos de ponta a ponta, desde a concepção teórica até a implementação prática.


**Tecnologias utilizadas:**  
- Linguagem de programação: **Python**
- Frameworks: **Django, Ultralytics YOLOv8, OpenCV**
- Banco de dados: **MySQL**  
- Bibliotecas: **PyTorch, NumPy, PyMySQL**
- Ambiente de desenvolvimento: **Google Colab (GPU: Tesla T4) para treinamento, Linux (Ubuntu) para desenvolvimento local**  
- Ferramentas auxiliares: **Roboflow para gerenciamento e anotação de datasets; Git para versionamento**

**Escopo do projeto:**  
- Desenvolvimento de um sistema automatizado de **detecção de EPIs** baseado em imagens, com aplicação direta na **prevenção de acidentes de trabalho**.  
- Treinamento e avaliação de modelos YOLOv8 em diferentes configurações (Nano, Small, Medium, Large) para identificar objetos como: capacetes, luvas, óculos, calçados de segurança, coletes, entre outros.  
- Criação de um **dataset próprio** com mais de 6 mil imagens anotadas, utilizando técnicas de **data augmentation**.  
- Integração do modelo de detecção com uma aplicação web desenvolvida em Django, oferecendo uma interface acessível e funcional.  
- Implementação de **streaming de vídeo** com detecção em tempo real utilizando **OpenCV**.

**Desafios enfrentados e aprendizados:**  
- **Fine-tuning** de hiperparâmetros para balancear **precisão** e **eficiência computacional**.  
- Tratamento de **class imbalance** e dificuldade na detecção de objetos pequenos como luvas e botas.  
- Integração complexa entre o pipeline de visão computacional e a arquitetura **MVT** do Django.  
- Considerações éticas sobre **privacy** e **data security** em ambientes industriais.  

**Pontos que poderiam ser aprimorados futuramente:**  
- Aumento e diversificação do dataset, especialmente para classes minoritárias.  
- Implementação de **automated tests** para garantir a robustez da aplicação.  
- Otimização de desempenho para **inference on edge devices**.  
- Uso de containers **Docker** para facilitar o deployment e escalabilidade da aplicação.  
- Adoção de práticas de **MLOps** para gerenciamento do ciclo de vida do modelo.

**Reflexão pessoal:**  
Este projeto representa um **marco fundamental** na minha trajetória como desenvolvedor e pesquisador, consolidando conhecimentos em **Deep Learning**, **desenvolvimento backend**, **banco de dados** e **infraestrutura de sistemas**. Além disso, proporcionou uma compreensão profunda sobre os desafios reais de implementar soluções de IA aplicadas à segurança no trabalho.

**Observação:**  
Para outros projetos que ilustram a minha evolução e consolidação em engenharia de software e inteligência artificial, consulte os demais repositórios disponíveis no meu portfólio.

### 🇬🇧 English

This project was developed as part of my **Undergraduate Thesis** in Computer Science at FEMA - Fundação Educacional do Município de Assis. The project presents a practical application of **Computer Vision** and **Artificial Intelligence** to promote **workplace safety** through the automatic detection of **Personal Protective Equipment (PPE)** using the **YOLOv8** model.

**Reason for keeping this project active:**  
Unlike projects that I preserve in their original state, this project remains active as a representative example of my current ability to integrate **Machine Learning**, **web development**, and **software engineering**. I chose to keep it public and well-documented as evidence of my technical competence and ability to manage projects end-to-end, from theoretical design to practical implementation.

**Technologies used:**  
- Programming language: **Python**  
- Frameworks: **Django, Ultralytics YOLOv8, OpenCV**  
- Database: **MySQL**  
- Libraries: **PyTorch, NumPy, PyMySQL**  
- Development environment: **Google Colab (GPU: Tesla T4) for model training, Linux (Ubuntu) for local development**
- Auxiliary tools: **Roboflow for dataset management and annotation; Git for version control**  

**Project scope:**  
- Development of an automated **PPE detection system** based on image processing, directly applied to **workplace accident prevention**.  
- Training and evaluation of YOLOv8 models in different configurations (Nano, Small, Medium, Large) to identify objects such as helmets, gloves, glasses, safety boots, vests, among others.  
- Creation of a **proprietary dataset** with over 6,000 annotated images, employing **data augmentation** techniques.  
- Integration of the detection model with a web application built in Django, offering an accessible and functional interface.  
- Implementation of **real-time video streaming** with detection using **OpenCV**.

**Challenges faced and key learnings:**  
- **Fine-tuning** of hyperparameters to balance **accuracy** and **computational efficiency**.  
- Handling **class imbalance** and the difficulty of detecting small objects such as gloves and boots.  
- Complex integration between the computer vision pipeline and Django's **MVT** architecture.  
- Ethical considerations regarding **privacy** and **data security** in industrial environments.

**Areas for future improvement:**  
- Expansion and diversification of the dataset, especially for underrepresented classes.  
- Implementation of **automated tests** to ensure application robustness.  
- Performance optimization for **inference on edge devices**.  
- Use of **Docker** containers for easier deployment and application scalability.  
- Adoption of **MLOps practices** for comprehensive model lifecycle management.

**Personal reflection:**  
This project represents a **key milestone** in my journey as a developer and researcher, consolidating my knowledge in **Deep Learning**, **backend development**, **databases**, and **system infrastructure**. It also provided me with a deep understanding of the real-world challenges in deploying AI solutions for workplace safety.

**Note:**  
For other projects reflecting my ongoing evolution and consolidation in software engineering and artificial intelligence, please refer to the other repositories available in my portfolio.

## ⚙️ COMO EXECUTAR | HOW TO RUN 
### Clone Project
To clone the project from Github you'll need to use this command.
```shell
$ git clone https://github.com/gabrielmossini/tcc.git
```
### Python and Django configuration
First you need to install the repositories, if you're using Ubuntu or Debian based, you can verify using the following command.
```shell
$ python3 -V
```
Create a virtual enviroment inside the tcc/Aegis folder.
```shell
$ python3 -m venv venv
```
This install a virtual version of Python, pip within your project directory. To install any packges into the project, you must activate the enviroment using the following command.
```shell
$ source venv/bin/activate
```
Your shell prompt will change to reflect the virtual enviroment.
```shell
$ (venv) user@device:~/Aegis$
```
Now the virtual environment is activated, use <i>pip</i> to install Django. To install all the pips required you'll need to use this command inside the main project folder.
```shell
$ pip install -r requirements.txt
```
Verify the installation.
```shell
$ (venv) $ django-admin --version
output: 5.1.6 
```
#### Repository Default User Configuration
All you're gonna need to do is two commands the first one:
```shell
$ python3 manage.py makemigrations
```
And the second one:
```shell
$ python3 manage.py migrate
```
Now you gonna need to create a default user, following this command.
```shell
$ python3 manage.py create_default_user
```

The user created is:
- User: <i> default </i>
- Password: <i> password123 </i>

## Run
Now to run the app you're gonna to write this command in the terminal:
```shell
$ python3 manage.py runserver
```
