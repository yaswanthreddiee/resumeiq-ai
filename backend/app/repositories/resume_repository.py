from datetime import datetime

from bson import ObjectId


class ResumeRepository:
    """
    Repository responsible for all Resume database operations.
    """

    def __init__(self, db):
        self.resume_collection = db.resumes
        self.analysis_collection = db.analyses
        self.job_match_collection = db.job_matches

    # --------------------------------------------------
    # Resume
    # --------------------------------------------------

    async def create_resume(
        self,
        user_id: str,
        filename: str,
        stored_path: str,
        parsed_content: dict,
    ):

        document = {
            "user_id": ObjectId(user_id),
            "file_name": filename,
            "file_url": stored_path,
            "parsed_content": parsed_content,
            "ats_score": None,
            "uploaded_at": datetime.utcnow(),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = await self.resume_collection.insert_one(document)

        document["_id"] = result.inserted_id

        return document

    async def get_resume(
        self,
        resume_id: str,
        user_id: str,
    ):

        return await self.resume_collection.find_one(
            {
                "_id": ObjectId(resume_id),
                "user_id": ObjectId(user_id),
            }
        )

    async def list_resumes(
        self,
        user_id: str,
    ):

        return await self.resume_collection.find(
            {
                "user_id": ObjectId(user_id),
            }
        ).sort(
            "created_at",
            -1,
        ).to_list(None)

    async def delete_resume(
        self,
        resume_id: str,
        user_id: str,
    ):

        return await self.resume_collection.find_one_and_delete(
            {
                "_id": ObjectId(resume_id),
                "user_id": ObjectId(user_id),
            }
        )

    async def update_ats_score(
        self,
        resume_id: str,
        ats_score: dict,
    ):

        await self.resume_collection.update_one(
            {
                "_id": ObjectId(resume_id),
            },
            {
                "$set": {
                    "ats_score": ats_score,
                    "updated_at": datetime.utcnow(),
                }
            },
        )

    # --------------------------------------------------
    # ATS Analysis
    # --------------------------------------------------

    async def save_ats_analysis(
        self,
        resume_id: str,
        user_id: str,
        analysis: dict,
    ):

        document = {
            "resume_id": ObjectId(resume_id),
            "user_id": ObjectId(user_id),
            **analysis,
            "created_at": datetime.utcnow(),
        }

        result = await self.analysis_collection.insert_one(
            document
        )

        document["_id"] = result.inserted_id

        return document

    async def get_ats_analysis(
        self,
        resume_id: str,
        user_id: str,
    ):

        return await self.analysis_collection.find_one(
            {
                "resume_id": ObjectId(resume_id),
                "user_id": ObjectId(user_id),
            },
            sort=[("created_at", -1)],
        )

    # --------------------------------------------------
    # Job Matching
    # --------------------------------------------------

    async def save_job_match(
        self,
        resume_id: str,
        user_id: str,
        job_description: str,
        result: dict,
    ):

        document = {
            "resume_id": ObjectId(resume_id),
            "user_id": ObjectId(user_id),
            "job_description": job_description,
            **result,
            "created_at": datetime.utcnow(),
        }

        insert = await self.job_match_collection.insert_one(
            document
        )

        document["_id"] = insert.inserted_id

        return document

    async def get_job_match(
        self,
        resume_id: str,
        user_id: str,
    ):

        return await self.job_match_collection.find_one(
            {
                "resume_id": ObjectId(resume_id),
                "user_id": ObjectId(user_id),
            },
            sort=[("created_at", -1)],
        )

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    async def delete_resume_related_data(
        self,
        resume_id: str,
    ):

        await self.analysis_collection.delete_many(
            {
                "resume_id": ObjectId(resume_id),
            }
        )

        await self.job_match_collection.delete_many(
            {
                "resume_id": ObjectId(resume_id),
            }
        )