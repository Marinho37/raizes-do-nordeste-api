import uvicorn
from multiprocessing import Process
import time, requests, json

def start_server():
    uvicorn.run('app.main:app', host='127.0.0.1', port=8000, log_level='error')

if __name__ == '__main__':
    p = Process(target=start_server)
    p.start()
    time.sleep(3)
    
    # Run tests
    try:
        # DB Setup para Unidade e Estoque antes de testar a API via SQLite ou requests.
        import sqlite3
        conn = sqlite3.connect('raizes_nordeste.db')
        c = conn.cursor()
        c.execute("INSERT INTO unidades (nome, endereco) VALUES ('Matriz Recife', 'Rua A')")
        unidade_id = c.lastrowid
        conn.commit()
        conn.close()

        # Register a test admin user first so we can log in
        requests.post('http://localhost:8000/auth/registrar', json={'nome':'admin', 'email':'admin@raizes.com', 'senha':'123456', 'perfil':'ADMIN'})
        
        # Test 1
        r = requests.post('http://localhost:8000/auth/login', json={'email':'admin@raizes.com','senha':'123456'})
        assert r.status_code == 200, f"Failed T01: {r.status_code} {r.text}"
        token = r.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print('T01 Pass')
        
        # Test 2
        r = requests.get('http://localhost:8000/pedidos/')
        assert r.status_code == 401, f"Failed T02: {r.status_code} {r.text}"
        print('T02 Pass')
        
        # Test 3
        r = requests.get('http://localhost:8000/produtos/')
        assert r.status_code == 200, f"Failed T03: {r.status_code} {r.text}"
        print('T03 Pass')
        
        # Test 4
        r = requests.post('http://localhost:8000/produtos/', json={'nome':'Tapioca', 'descricao':'Tapioca de queijo', 'preco':15.0})
        assert r.status_code == 401, f"Failed T04: {r.status_code} {r.text}"
        print('T04 Pass')
        
        # Add a product validly to test orders
        r = requests.post('http://localhost:8000/produtos/', json={'nome':'Tapioca', 'descricao':'Tapioca de queijo', 'preco':15.0}, headers=headers)
        produto_id = r.json()['id']

        # Add stock via SQL as we need it for T06 and T11
        conn = sqlite3.connect('raizes_nordeste.db')
        c = conn.cursor()
        c.execute("INSERT INTO estoque (produto_id, unidade_id, quantidade) VALUES (?, ?, ?)", (produto_id, unidade_id, 2))
        conn.commit()
        conn.close()
        
        # Test 5 - Pedido sem canalPedido (422)
        r = requests.post('http://localhost:8000/pedidos/', json={'unidade_id': unidade_id, 'itens':[{'produto_id':produto_id,'quantidade':2}]}, headers=headers)
        assert r.status_code == 422, f"Failed T05: {r.status_code} {r.text}"
        print('T05 Pass')
        
        # Test 6 - Pedido Valido -> 201 (estoque reduzirá de 2 para 1)
        r = requests.post('http://localhost:8000/pedidos/', json={'unidade_id': unidade_id, 'canalPedido':'APP','itens':[{'produto_id':produto_id,'quantidade':1}]}, headers=headers)
        assert r.status_code == 201, f"Failed T06: {r.status_code} {r.text}"
        print('T06 Pass')
        
        # Test 7 - Pedido Produto Inexistente (404)
        r = requests.post('http://localhost:8000/pedidos/', json={'unidade_id': unidade_id, 'canalPedido':'APP','itens':[{'produto_id':999,'quantidade':1}]}, headers=headers)
        assert r.status_code == 404, f"Failed T07: {r.status_code} {r.text}"
        print('T07 Pass')
        
        # Test 8 - Pagamento MOCK Ok (200)
        r = requests.post('http://localhost:8000/pagamentos/', json={'pedido_id': 1, 'forma_pagamento':'MOCK'}, headers=headers)
        assert r.status_code == 200, f"Failed T08: {r.status_code} {r.text}"
        print('T08 Pass')
        
        # Test 9: Create new order then fail payment (400) - stock goes 1 -> 0
        r = requests.post('http://localhost:8000/pedidos/', json={'unidade_id': unidade_id, 'canalPedido':'APP','itens':[{'produto_id':produto_id,'quantidade':1}]}, headers=headers)
        r = requests.post('http://localhost:8000/pagamentos/', json={'pedido_id': 2, 'forma_pagamento':'CARTAO_INVALIDO'}, headers=headers)
        assert r.status_code == 400, f"Failed T09: {r.status_code} {r.text}"
        print('T09 Pass')
        
        # Test 10 - Filter Pedidos by Canal
        r = requests.get('http://localhost:8000/pedidos/?canalPedido=APP', headers=headers)
        assert r.status_code == 200, f"Failed T10: {r.status_code} {r.text}"
        print('T10 Pass')

        # Test 11 - Estoque insuficiente (409) - Stock is 0 now
        r = requests.post('http://localhost:8000/pedidos/', json={'unidade_id': unidade_id, 'canalPedido':'APP','itens':[{'produto_id':produto_id,'quantidade':1}]}, headers=headers)
        assert r.status_code == 409, f"Failed T11: {r.status_code} {r.text}"
        print('T11 Pass')

        print('ALL TESTS PASSED!')
    except Exception as e:
        print('ERROR:', e)
    finally:
        p.terminate()
