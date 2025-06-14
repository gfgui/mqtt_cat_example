# 📡 Projeto MQTT - Sistemas Distribuídos

> 💻 **Trabalho de Invocação Remota e Comunicação Indireta**  
> 🎓 Disciplina: Sistemas Distribuídos

---

## 📘 Descrição

Este projeto demonstra a utilização do protocolo **MQTT** para comunicação indireta entre sensores e um monitor de alarmes, como parte de um trabalho acadêmico.

A comunicação é feita via **publicação e assinatura de tópicos**, com foco na **invocação remota desacoplada** de tempo, espaço e sincronização.

---

## ⚙️ Tecnologias Utilizadas

- 🐍 Python  
- 📡 [Paho MQTT](https://www.eclipse.org/paho/) (cliente MQTT)
- 🐞 Mosquitto (broker MQTT)

---

## 🔧 Funcionalidades

- Simulação de múltiplos sensores que publicam temperatura em tópicos distintos
- Detecção de:
  - 🔥 Temperatura alta (`> 200ºC`)
  - ⚠️ Mudanças bruscas de temperatura (variação ≥ 5ºC)
- Interface gráfica com histórico de alertas e sinal sonoro (via `Tkinter`)
- Sensores com comportamento realista (reconexão e inicialização assíncrona)

---

## 📺 Demonstração

🎥 Um vídeo demonstrando o funcionamento do sistema está disponível dentro do próprio repositório.  
Abra o arquivo ou assista via o player embutido.

---
