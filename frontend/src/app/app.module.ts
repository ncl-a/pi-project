import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HttpClient } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FooterComponent } from './widget/footer/footer.component';
import { SidebarComponent } from './widget/sidebar/sidebar.component';
import { HeaderComponent } from './widget/header/header.component';
import { HomeComponent } from './page/home/home.component';
import { PageNotFoundComponent } from './page/page-not-found/page-not-found.component';
import { TaskPreviewComponent } from './widget/task/task-preview/task-preview.component';
import { TaskPreviewListComponent } from './widget/task/task-preview-list/task-preview-list.component';

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    SidebarComponent,
    HeaderComponent,
    HomeComponent,
    PageNotFoundComponent,
    TaskPreviewComponent,
    TaskPreviewListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
