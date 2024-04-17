<?php

namespace App\Enums;

enum TaskStatus: string
{
    const todo = "todo";
    const progress = "progress";
    const done = "done";
}
