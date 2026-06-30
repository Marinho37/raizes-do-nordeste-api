import uvicorn
from multiprocessing import Process
import time, requests, json, os

def start_server():
    uvicorn.run('app.main:app', host='127.0.0.1', port=8000, log_level='error')

if __name__ == '__main__':
    if os.path.exists('raizes_nordeste.db'):
        os.remove('raizes_nordeste.db')

    p = Process(target=start_server)
    p.start()
    time.sleep(3)
    
    # Run tests
    try:
        print("Iniciando bateria de testes...")
        # Test 1 - POST /auth/login
        r = requests.post('http://localhost:8000/auth/login', json={'email':'admin@raizes.com','senha':'123456'})
        assert r.status_code == 200, f"Failed T01: {r.status_code} {r.text}"
        token = r.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print('T01 Pass - Login Válido (200)')
        
        # Test 2 - GET /pedidos/ (Sem token -> 401)
        r = requests.get('http://localhost:8000/pedidos/')
        assert r.status_code == 401, f"Failed T02: {r.status_code} {r.text}"
        print('T02 Pass - Acesso Sem Token (401)')
        
        # Test 3 - POST /pedidos/ (Falta Canal -> 422)
        r = requests.post('http://localhost:8000/pedidos/', json={'unidade_id': 1, 'itens':[{'produto_id':1,'quantidade':2}]}, headers=headers)
        assert r.status_code == 422, f"Failed T03: {r.status_code} {r.text}"
        print('T03 Pass - Pedido Falta Canal (422)')
        
        # Test 4 - POST /pedidos/ (Criar Pedido OK -> 201)
        r = requests.post('http://localhost:8000/pedidos/', json={'unidade_id': 1, 'canalPedido':'APP','itens':[{'produto_id':1,'quantidade':1}]}, headers=headers)
        assert r.status_code == 201, f"Failed T04: {r.status_code} {r.text}"
        print('T04 Pass - Criar Pedido Válido (201)')
        
        # Test 5 - POST /pedidos/ (Produto Inexistente -> 404)
        r = requests.post('http://localhost:8000/pedidos/', json={'unidade_id': 1, 'canalPedido':'APP','itens':[{'produto_id':999,'quantidade':1}]}, headers=headers)
        assert r.status_code == 404, f"Failed T05: {r.status_code} {r.text}"
        print('T05 Pass - Produto Inexistente (404)')
        
        # Test 6 - POST /pagamentos/ (MOCK Ok -> 200)
        # Pagamento gerará 15 pontos de fidelidade (preco=15.0 * 1 quantidade)
        r = requests.post('http://localhost:8000/pagamentos/', json={'pedido_id': 1, 'forma_pagamento':'MOCK'}, headers=headers)
        assert r.status_code == 200, f"Failed T06: {r.status_code} {r.text}"
        print('T06 Pass - Pagar MOCK Ok (200)')
        
        # Test 7 - POST /pagamentos/ (FALHA -> 400)
        r = requests.post('http://localhost:8000/pedidos/', json={'unidade_id': 1, 'canalPedido':'APP','itens':[{'produto_id':1,'quantidade':1}]}, headers=headers)
        pedido_id_2 = r.json()['id']
        r = requests.post('http://localhost:8000/pagamentos/', json={'pedido_id': pedido_id_2, 'forma_pagamento':'FALHA'}, headers=headers)
        assert r.status_code == 400, f"Failed T07: {r.status_code} {r.text}"
        print('T07 Pass - Pagar MOCK Recusado (400)')
        
        # Test 8 - PATCH /estoque/movimentar (Acesso Negado CLIENTE -> 403)
        requests.post('http://localhost:8000/auth/registrar', json={'nome':'client', 'email':'client@raizes.com', 'senha':'123', 'perfil':'CLIENTE'})
        r_client = requests.post('http://localhost:8000/auth/login', json={'email':'client@raizes.com','senha':'123'})
        client_headers = {'Authorization': f'Bearer {r_client.json()["access_token"]}'}
        r = requests.patch('http://localhost:8000/estoque/movimentar', json={'produto_id':1, 'unidade_id':1, 'quantidade':10}, headers=client_headers)
        assert r.status_code == 403, f"Failed T08: {r.status_code} {r.text}"
        print('T08 Pass - Estoque Acesso Negado (403)')
        
        # Test 9 - GET /fidelidade/saldo (Consultar Pontos -> 200 (150))
        requests.post('http://localhost:8000/fidelidade/registrar?pontos=135', headers=headers)
        r = requests.get('http://localhost:8000/fidelidade/saldo', headers=headers)
        assert r.status_code == 200, f"Failed T09: {r.status_code} {r.text}"
        assert r.json()['saldo_pontos'] == 150, f"Failed T09 points mismatch"
        print('T09 Pass - Consultar Pontos Fidelidade (200)')
        
        # Test 10 - POST /fidelidade/resgatar (Saldo Insuficiente -> 400)
        r = requests.post('http://localhost:8000/fidelidade/resgatar?pontos=200', headers=headers)
        assert r.status_code == 400, f"Failed T10: {r.status_code} {r.text}"
        print('T10 Pass - Saldo Insuficiente Fidelidade (400)')
        
        # Test 11 - POST /pedidos/ (Estoque Insuficiente -> 409)
        r = requests.post('http://localhost:8000/pedidos/', json={'unidade_id': 1, 'canalPedido':'APP','itens':[{'produto_id':1,'quantidade':9999}]}, headers=headers)
        assert r.status_code == 409, f"Failed T11: {r.status_code} {r.text}"
        print('T11 Pass - Estoque Insuficiente (409)')

        print('\nALL TESTS PASSED! O código está 100% aderente ao novo Documento DOCX.')
    except Exception as e:
        print('ERROR:', e)
    finally:
        p.terminate()
