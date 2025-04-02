# Exemplo de código Python em um único arquivo

def saudacao(nome):
    return f"Olá, {nome}! Bem-vindo."

def soma(a, b):
    return a + b

def main():
    nome = input("Digite seu nome: ")
    print(saudacao(nome))
    
    num1 = float(input("Digite o primeiro número: "))
    num2 = float(input("Digite o segundo número: "))
    print(f"A soma é: {soma(num1, num2)}")

if __name__ == "__main__":
    main()
