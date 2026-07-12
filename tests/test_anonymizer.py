from app.services.anonymizer import anonymize_text, anonymize_conversation

def test_anonymize_text_cpf():
    """Verify that Brazilian CPFs are correctly masked with <CPF>."""
    text = "Meu CPF é 123.456.789-00 ou 98765432100"
    anon = anonymize_text(text)
    assert "123.456.789-00" not in anon
    assert "98765432100" not in anon
    assert "<CPF>" in anon

def test_anonymize_text_email():
    """Verify that email addresses are masked with <EMAIL_ADDRESS>."""
    text = "Entre em contato pelo email teste@example.com por favor"
    anon = anonymize_text(text)
    assert "teste@example.com" not in anon
    assert "<EMAIL_ADDRESS>" in anon

def test_anonymize_text_phone():
    """Verify that phone numbers are masked with <PHONE_NUMBER>."""
    text = "Meu telefone é +55 11 99999-9999"
    anon = anonymize_text(text)
    assert "11 99999-9999" not in anon
    assert "<PHONE_NUMBER>" in anon

def test_anonymize_conversation():
    """Verify that full conversation message lists are anonymized while preserving prefixes."""
    messages = [
        "human: Olá, meu email é joao@gmail.com e meu CPF é 111.222.333-44",
        "ai: Recebido. Entraremos em contato em joao@gmail.com"
    ]
    anon_msgs = anonymize_conversation(messages)
    assert len(anon_msgs) == 2
    assert anon_msgs[0].startswith("human:")
    assert anon_msgs[1].startswith("ai:")
    assert "joao@gmail.com" not in anon_msgs[0]
    assert "111.222.333-44" not in anon_msgs[0]
    assert "joao@gmail.com" not in anon_msgs[1]
    assert "<EMAIL_ADDRESS>" in anon_msgs[0]
    assert "<CPF>" in anon_msgs[0]
    assert "<EMAIL_ADDRESS>" in anon_msgs[1]
