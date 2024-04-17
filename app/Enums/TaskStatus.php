<?php

namespace App\Enums;

enum TaskStatus: string
{
    case Todo = 'todo';
    case Progress = 'progress';
    case Done = 'done';
}
