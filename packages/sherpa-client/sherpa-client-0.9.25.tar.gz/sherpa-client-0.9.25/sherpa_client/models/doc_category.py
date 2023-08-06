from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.doc_category_status import DocCategoryStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocCategory")


@attr.s(auto_attribs=True)
class DocCategory:
    """A document category"""

    label_name: str
    identifier: Union[Unset, str] = UNSET
    score: Union[Unset, float] = UNSET
    status: Union[Unset, DocCategoryStatus] = UNSET
    created_date: Union[Unset, str] = UNSET
    modified_date: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label_name = self.label_name
        identifier = self.identifier
        score = self.score
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        created_date = self.created_date
        modified_date = self.modified_date
        created_by = self.created_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "labelName": label_name,
            }
        )
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if score is not UNSET:
            field_dict["score"] = score
        if status is not UNSET:
            field_dict["status"] = status
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if modified_date is not UNSET:
            field_dict["modifiedDate"] = modified_date
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label_name = d.pop("labelName")

        identifier = d.pop("identifier", UNSET)

        score = d.pop("score", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, DocCategoryStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = DocCategoryStatus(_status)

        created_date = d.pop("createdDate", UNSET)

        modified_date = d.pop("modifiedDate", UNSET)

        created_by = d.pop("createdBy", UNSET)

        doc_category = cls(
            label_name=label_name,
            identifier=identifier,
            score=score,
            status=status,
            created_date=created_date,
            modified_date=modified_date,
            created_by=created_by,
        )

        return doc_category
