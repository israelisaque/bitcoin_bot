import ssl
import json

import rel
import websocket
import bitstamp.client

import credenciais


def cliente():
    return bitstamp.client.Trading(username=credenciais.USERNAME,
                                   key=credenciais.KEY,
                                   secret=credenciais.SECRET)


def comprar(quantidade):
    trading_client = cliente()
    trading_client.buy_market_order(quantidade)


def vender(quantidade):
    trading_client = cliente()
    trading_client.sell_market_order(quantidade)


def ao_abrir(ws):
    print("Abriu a conexão")

    json_subscribe = """
{
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}                
    """
    ws.send(json_subscribe)


def ao_fechar(ws):
    print("Fechou a conexão")


def erro(ws, erro):
    print("Deu erro")
    print(erro)


def ao_receber_mensagem(ws, mensagem):
    print(mensagem)


if __name__ == '__main__':
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net",
                                on_open=ao_abrir,
                                on_close=ao_fechar,
                                on_message=ao_receber_mensagem,
                                on_error=erro)

    ws.run_forever(dispatcher=rel, sslopt={"cert_reqs": ssl.CERT_NONE})  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

