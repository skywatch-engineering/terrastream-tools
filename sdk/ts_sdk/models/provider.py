#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import os

from pydantic import BaseModel
from pydantic import Field


class ConfigModel(BaseModel):
    """
    {
        "name": "provider_name",
        "username": "foo",
        "password": "bar",
        "base_url": "https://api.provider.domain.com/api",
    }
    """

    name: str = Field(..., description="Terrastream account user name")
    username: str = Field(..., description="Terrastream account user name")
    password: str = Field(..., description="Terrastream account password")
    base_url: str = Field(..., description="Terrastream base account url")
