from pydantic_ai import Agent
from pydantic import BaseModel
import yfinance as yf
import gradio as gr 

class StockPriceResult(BaseModel):
    symbol: str 
    price: float
    currency: str = "USD"
    message: str

stock_agent = Agent(
    "groq:llama3-groq-70b-8192-tool-use-preview",
    result_type=StockPriceResult,
    system_prompt="You are a helpful financial assistant that can look up stock prices. Use the get_stock_price tool to fetch current data."
)

@stock_agent.tool_plain
def get_stock_price(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info.last_price
    return {
        "price": round(price, 2),
        "currency": "USD"
    }
def get_stock_info(query):
    try:
        result = stock_agent.run_sync(query)
        response = f" Stock: {result.data.symbol}\n"
        response += f" Price: ${result.data.price:.2f} {result.data.currency}\n"
        response += f"\n{result.data.message}"
        return response
    except Exception as e:
        return f"Error: {str(e)}"

demo = gr.Interface(
    fn=get_stock_info,
    inputs=gr.Textbox(label="Ask about any stock price", placeholder="What is Apple's current stock price?"),
    outputs=gr.Textbox(label="Stock Information"),
    title="Stock Price AI Assistant",
    description="Ask me about any stock price and I'll fetch the latest information for you!"
)

if __name__ == "__main__":
    demo.launch()