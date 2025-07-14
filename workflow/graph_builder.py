from langgraph.graph import StateGraph, END
from models.trip_state import TripState
from agents.call_tools import call_tools
from agents.user_input_parse import parse_user_input
from agents.summary_agent import generate_response


def build_graph():
    workflow = StateGraph(TripState)

    
    workflow.add_node("parse_user_input", parse_user_input)
    workflow.add_node("call_tools", call_tools)
    workflow.add_node("generate_response", generate_response)

    
    workflow.set_entry_point("parse_user_input")

    
    workflow.add_edge("parse_user_input", "call_tools")
    workflow.add_edge("call_tools", "generate_response")
    workflow.add_edge("generate_response", END) 

    
    app = workflow.compile()
    return app

trip_planner_graph = build_graph()

def run_trip_planner_graph(user_query: str) -> TripState:
    """
    Runs the trip planner workflow and returns the final state.
    """
    initial_state = TripState(
        user_input=user_query,
        location=None,
        start_date=None,
        end_date=None,
        current_weather=None,
        current_weather_temp=None,
        current_weather_condition=None,
        forecast_weather=None,
        forecast_weather_min_temp=None,
        forecast_weather_max_temp=None,
        forecast_weather_condition=None,
        attractive_place=None,
        hotel_info=None,
        no_of_traveler=None,
        from_currency=None,
        to_currency=None,
        rate=None,
        budget_usd=None,
        local_currency_budget=None,
        status="initial",
        messages=[{"role": "user", "content": user_query}],
        final_plan=None
    )
    
    final_state = initial_state
    for s in trip_planner_graph.stream(initial_state):
        for key, value in s.items():
            final_state = value 
    
    return final_state