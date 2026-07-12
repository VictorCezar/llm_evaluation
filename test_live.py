import json
import urllib.request
import urllib.error
import sys

def main():
    # Mock conversation from exemplo_conversas.json (sessionId S_de744131)
    mock_payload = {
        "sessionId": "S_de744131",
        "messages": [
            "human: Eu sou Pessoa_003",
            "ai: Olá, Pessoa_003, eu sou a Beatriz, consultora de carreira da +A Code Academy. Vi que você tem interesse em uma pós-graduação. Me conta: você já tem um curso em mente?",
            "human: A descrição da imagem é: Na imagem aparece um fundo roxo com uma textura de grade digital. No topo esta escrito pos+A Code Academydigital e logo ao lado tem um simbolo da IES. No centro em um quadro destaca o curso pos em marketing negocios digitais e experiencia do cliente. Do lado esquerdo do quadro tem um icon de selo e o texto garanta a relevancia do selo +A Code Academy no seu curriculo em 12 meses. Do lado direito do quadro tem um selo redondo escrito pos graduacao. Logo abaixo esta escrito faca sua matricula e acelere sua carreira. Em destaque tem um botao branco com o texto de o primeiro passo com um link e emoji de explosao. Embaixo mostra seguido por rayannemenezes e outras 274 mil pessoas. No rodape aparece patrocinado com um coracao.",
            "human: Quanto está custando a mensalidade?",
            "ai: Entendi seu interesse pelo curso Marketing, Negócios Digitais e Experiência do Cliente. Muitos profissionais buscam essa especialização para se destacar no mercado digital.\nPara te ajudar melhor, qual é seu principal objetivo ao fazer essa pós?",
            "ai: Sobre valores da mensalidade, vou te conectar direto com um especialista que pode te informar todos os detalhes do investimento. Quer que eu faça essa transferência agora para que você já saiba tudo sobre as condições de pagamento?"
        ]
    }

    url = "http://localhost:8000/evaluate"

    print("=" * 60)
    print("VALIDAÇÃO FUNCIONAL - LLM-AS-A-JUDGE")
    print("=" * 60)
    print(f"Enviando requisição POST para {url}...")
    print(f"Session ID: {mock_payload['sessionId']}")
    print(f"Total de mensagens enviadas: {len(mock_payload['messages'])}")
    print("-" * 60)

    data = json.dumps(mock_payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.status
            response_data = response.read().decode("utf-8")
            result = json.loads(response_data)
            
            print(f"Sucesso! Código de status HTTP: {status_code}\n")
            print("=== Avaliação (ScorecardResponse) Gerada pelo LLM ===")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print("=" * 60)
    except urllib.error.HTTPError as e:
        print(f"Erro HTTP {e.code}: {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Erro de Conexão: Não foi possível conectar à API.", file=sys.stderr)
        print("Certifique-se de que a API está rodando no contêiner ou localmente na porta 8000.", file=sys.stderr)
        print(f"Detalhe do erro: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
