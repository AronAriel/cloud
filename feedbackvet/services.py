from models import Feedback


def serialize_feedback(feedback):
    return {
        "id": feedback.id,
        "consultation_id": feedback.consultation_id,
        "rating": feedback.rating,
        "comment": feedback.comment,
    }


def list_feedbacks(db):
    feedbacks = db.query(Feedback).all()
    return [serialize_feedback(feedback) for feedback in feedbacks]


def consume_service_bus_messages(receiver, logger):
    messages = receiver.receive_messages(max_message_count=10)

    for message in messages:
        logger.info(f"Received message: {message}")
        receiver.complete_message(message)

    return len(messages)
