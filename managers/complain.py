from db import database
from models import complaint, RoleType, State


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        query = complaint.select()
        if user["role"] == RoleType.complainer:
            query = query.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            query = query.where(complaint.c.state == State.pending)
        return await database.fetch_all(query)

    @staticmethod
    async def create_complaint(request, complaint_data):
        complaint_data["complainer_id"] = request.state.user.id
        id_ = await database.execute(complaint.insert().values(**complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete_complaint(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def approve(complaint_id):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == complaint_id)
            .values(status=State.approved)
        )

    @staticmethod
    async def reject(complaint_id):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == complaint_id)
            .values(status=State.rejected)
        )
