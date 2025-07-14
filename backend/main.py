from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from models.trip_state import TripState, TripRequest
from workflow.graph_builder import run_trip_planner_graph

app = FastAPI(
    title="Trip Planner API",
    description="API for planning trips using AI and external tools."
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trip Planner API</title>
    </head>
    <body>
        <h1>Welcome to the Trip Planner API!</h1>
        <p>Use the <code>/plan_trip</code> endpoint to plan your next adventure.</p>
        <p>Example: <code>POST /plan_trip</code> with JSON body: <code>{"user_query": "Plan a trip to Paris from July 20, 2025 to July 25, 2025 for 2 people with a budget of 3000 USD. I want to convert USD to EUR."}</code></p>
        <p>Access the API documentation at <a href="/docs">/docs</a></p>
        <p>If you have Streamlit installed, you can run the frontend using: <code>streamlit run frontend/main.py</code></p>
    </body>
    </html>
    """

@app.post("/plan_trip", response_model=TripState)
async def plan_trip(request: TripRequest):
    """
    Plans a trip based on the user's query using an AI agent.
    """
    try:
        final_state = run_trip_planner_graph(request.user_query)
        response_data = dict(final_state) 
    
        if not response_data.get('final_plan'): 
            if response_data.get('status') == 'completed':
                last_assistant_message = next((msg['content'] for msg in reversed(response_data.get('messages', [])) if msg['role'] == 'assistant'), None)
                if last_assistant_message:
                    response_data['final_plan'] = last_assistant_message
                else:
                    response_data['final_plan'] = "Could not generate a detailed plan, but graph completed. No assistant message found."
            else:
                
                response_data['final_plan'] = f"Could not generate a detailed plan. Status: {response_data.get('status', 'unknown')}. Please check the messages for more details."

       
        if 'messages' not in response_data or response_data['messages'] is None:
            response_data['messages'] = []
        return TripState(**response_data)
        
    except Exception as e:
        
        print(f"Unhandled error in plan_trip endpoint: {e}", exc_info=True) 
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during trip planning: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)