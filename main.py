from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()

class TicketCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title : str =Field(min_length=1, max_length=100)
    description : str = Field(min_length=1, max_length=100)

class TicketUpdate(BaseModel):
    status : str


tickets = [{
    "id":1,
    "title": "Wi-Fi is not working",
    "description": "My laptop cannot connect",
    "status": "open"
}]

next_ticket_id = 2


@app.get("/")
def home():
    return{
        "message": "Welcome to the Help Desk Api."
    }

@app.get("/tickets")
def get_tickets():
    return tickets

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
            
    raise HTTPException(status_code=404, detail="Ticket not found")



@app.post("/tickets", status_code=201)
def create_ticket(ticket: TicketCreate):
    global next_ticket_id
    new_ticket = {
        "id": next_ticket_id,
        "title": ticket.title,
        "description": ticket.description,
        "status": "open"
    }
    tickets.append(new_ticket)
    next_ticket_id += 1
    return new_ticket


@app.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id : int, update: TicketUpdate):
    if update.status not in ["open", "in_progress", "resolved"]:
        raise HTTPException(status_code=400, detail="status must be open, in_progress or resolved")
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["status"] = update.status
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found.")


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticked_id : int):
    for ticket in tickets:
        if ticket["id"] == ticked_id:
            tickets.remove(ticket)
            return {"message": f"Ticker Id{ticked_id} deleted."}
    raise HTTPException(status_code=404, detail="ticket not found.")