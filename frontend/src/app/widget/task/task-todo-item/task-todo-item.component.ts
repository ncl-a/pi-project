import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TodoItemModel } from 'src/app/model/entity/todo-item.model';
import { TodoService } from 'src/app/service/api/entity/todo/todo.service';
import { UtilsService } from 'src/app/service/utils/utils.service';

@Component({
  selector: 'app-task-todo-item',
  templateUrl: './task-todo-item.component.html',
  styleUrls: ['./task-todo-item.component.scss']
})
export class TaskTodoItemComponent {

  constructor(public utilsService: UtilsService, private todoService: TodoService) {}

  @Input("item") item?: TodoItemModel;

  @Output() refreshRequest = new EventEmitter<void>();

  done() {

    if(!this.item)
      return;

    this.todoService.update(this.item.id, {
      done: !this.item.done
    }).then((response) => {
      response.subscribe({
        next: (value) => {
          this.refreshRequest.emit();
        }
      })
    })

  }
}
