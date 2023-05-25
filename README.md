# Telegram Reservation Bot

## Description
This Telegram bot is designed to facilitate and streamline the process of making reservations. It engages users in interactive conversations to gather necessary reservation details such as name, email address, and phone number. The bot offers a user-friendly and intuitive interface that makes it easy even for non-technical users to navigate and complete their reservations.

Key features of the bot include:

* **Interactive Reservation Creation:** The bot guides users through a step-by-step process to collect all necessary information for a reservation.

* **Error Handling**: The bot validates user input at each step to ensure all provided information is correct and complete.

* **Reservation Confirmation**: Upon the completion of the reservation process, the bot provides a summary of the reservation details for user confirmation.

* **ancellation and Restart**: Users have the option to cancel the reservation process at any point or restart it if they want to change any details.

## Conversation flow
1. Start: When the bot starts, it displays a keyboard with two options: "Create a reservation" and "Quit".

2. Choosing: If the user selects "Create a reservation", the bot moves to the create_reservation state and asks for the guest's name.
If the user types anything other than the provided options, the bot re-prompts the user with the initial options.
3. Name: The bot collects the guest's name. If the user types "Cancel", the conversation ends.
After collecting the name, the bot moves to the ask_email state.
4. Email: The bot collects the guest's email. If the user types "Cancel", the conversation ends.
After collecting the email, the bot asks the user to confirm the reservation or start over.
5. Finish Reservation: If the user types "Finish reservation", the bot moves to the done state and asks the user if they want to save the reservation.
If the user types "Start over", the bot clears all collected data and returns to the initial state.
6. Choice State: If the user responds with "Yes", the bot saves the reservation to the database.
If the user responds with "No", the bot does not save the reservation and ends the conversation.
7. Done: 
This state is reached when the user confirms the reservation details. If the user wants to save the reservation, the bot asks the user for confirmation ("Yes" or "No").
8. Fallbacks: If at any point the user types "Done", the bot ends the conversation.
If at any point the user types "Start over", the bot clears all collected data and starts over from the initial state.
If at any point the user types "Cancel", the bot ends the conversation.
