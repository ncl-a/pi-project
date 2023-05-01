import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TaskLabelModel } from 'src/app/model/entity/task-label.model';
import { TaskStatusModel } from 'src/app/model/entity/task-status.model';
import { TaskModel } from 'src/app/model/entity/task.model';
import { UpdateTaskModel } from 'src/app/model/entity/update-task.model';
import { UserModel } from 'src/app/model/entity/user.model';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { TaskStatusService } from 'src/app/service/api/entity/task-status/task-status.service';
import { TaskService } from 'src/app/service/api/entity/task/task.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';
import { LoggerService } from 'src/app/service/logger/logger.service';
import { UtilsService } from 'src/app/service/utils/utils.service';
import { environment } from 'src/environments/environment.development';

enum DeadlineStatus {
  PRIMARY,
  WARNING,
  DANGER
}

@Component({
  selector: 'app-task-preview',
  templateUrl: './task-preview.component.html',
  styleUrls: ['./task-preview.component.scss']
})
export class TaskPreviewComponent {

  @Input('task') task?: TaskModel;
  @Input("loggedUser") loggedUser?: UserModel;
  @Input("todoCollapseStatus") todoCollapseStatus: boolean = false;

  @Output() onDeletion = new EventEmitter<number>();
  @Output() onModify = new EventEmitter<UpdateTaskModel>();
  @Output() onRemoveAssignment = new EventEmitter<UpdateTaskModel>();
  @Output() onAddAssignment = new EventEmitter<UpdateTaskModel>();
  @Output() onRemoveLabel = new EventEmitter<UpdateTaskModel>();
  @Output() onAddLabel = new EventEmitter<UpdateTaskModel>();

  constructor(private taskService: TaskService, private authService: AuthService, public utilsService: UtilsService, private taskStatusService: TaskStatusService) {
  }

  nextStatus?: Promise<TaskStatusModel>;
  prevStatus?: Promise<TaskStatusModel>;

  ngOnInit() {

    if(this.task) {

      if(this.task.task_status) {

        if(this.task.task_status.default_next_task_status_id)
          this.nextStatus = this.taskStatusService.getTaskById(this.task.task_status.default_next_task_status_id);

        if(this.task.task_status.default_prev_task_status_id)
          this.prevStatus = this.taskStatusService.getTaskById(this.task.task_status.default_prev_task_status_id);
      }

    }


  }

  private _inModify: boolean = false;

  get inModify() {
    return this._inModify;
  }

  set inModify(value: boolean) {
    this._inModify = value;
  }

  userAssignedToTask(userId: number | undefined): boolean {

    if(!userId || !this.task)
      return false;


    let result = this.task.assigned_users?.map(au => au.user.id).includes(userId);

    if(result)
      return result;

    return false;
  }

  getAssignedUsers(): UserModel[] {

    return this.task?.assigned_users?.map(au => au.user) ?? [];

  }

  async removeUserFromTask(userId: number): Promise<void> {

    if(!this.task)
      return

    LoggerService.logInfo(`Removing user with id ${userId} from task: ${this.task.id} - ${this.task.name}`);

    const id = this.task.id;

    this.taskService.removeAssignment(id, userId).then((response) => {
      response.subscribe({
        next: (value: boolean) => {

          // refresh task
          this.taskService.find(id).then((respose) => {
            respose.subscribe({
              next: (t) => {
                this.task = t;
                this.onRemoveAssignment.emit({
                  target: id,
                  new: t
                });
              }
            })
          })

        }
      })
    });


  }

  async addAssignment(user: UserModel): Promise<void> {

    if(!this.task)
      return

    LoggerService.logInfo(`Add user ${user.username} to task: ${this.task.id} - ${this.task.name}`);

    const id = this.task.id;

    this.taskService.addAssignment(id, user.id).then((response) => {
      response.subscribe({
        next: (value: boolean) => {

          // refresh task
          this.taskService.find(id).then((respose) => {
            respose.subscribe({
              next: (t) => {
                this.task = t;
              }
            });
          })

        }
      })
    });


  }

  delete() {

    if(!this.task)
      return;

    LoggerService.logInfo("Remove task " + this.task?.name);

    const id = this.task.id;

    this.taskService.deleteById(id).then((response) => {
      response.subscribe({
        next: (value) => {
          this.onDeletion.emit(id);
        }
      })
    })
  }

  removeLabelFromTask(label: TaskLabelModel) {
    if(!this.task)
      return;

    LoggerService.logInfo("Remove label");

    const id = this.task.id;

    this.taskService.removeLabel(id, label.id).then((response) => {
      response.subscribe({
        next: (value) => {

          // refresh task
          this.taskService.find(id).then((respose) => {
            respose.subscribe({
              next: (t) => {
                this.task = t;
                this.onRemoveAssignment.emit({
                  target: id,
                  new: t
                });
              }
            })
          })
        }
      })
    });
  }

  addLabelToTask(label: TaskLabelModel) {
    if(!this.task)
      return;

    LoggerService.logInfo("Add label");

    const id = this.task.id;

    this.taskService.addLabel(id, label.id).then((response) => {
      response.subscribe({
        next: (value) => {


          // refresh task
          this.taskService.find(id).then((respose) => {
            respose.subscribe({
              next: (t) => {
                this.task = t;

              }
            })
          })
        }
      })
    });
  }

  modify(values: Object) {

    if(!this.task)
      return;

    LoggerService.logInfo("Modify task " + this.task?.name);

    const id = this.task.id;

    this.taskService.update(id, values).then((response) => {
      response.subscribe({
        next: (value) => {

          // refresh task
          this.taskService.find(id).then((respose) => {
            respose.subscribe({
              next: (t) => {
                this.task = t;

                this.onModify.emit({
                  target: id,
                  new: this.task
                })

              }
            })
          })

        }
      })
    })

  }
}
