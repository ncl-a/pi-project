export interface TaskStatusModel {
  id: number;
  name: string;
  description: string | null;

  default_next_task_status_id: number;
  default_next_task_status: TaskStatusModel | null;

  default_prev_task_status_id: number;
  default_prev_task_status: TaskStatusModel | null;
}
