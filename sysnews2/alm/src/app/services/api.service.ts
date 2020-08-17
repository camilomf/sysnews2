import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor( private http : HttpClient ) { 
    console.log("servicio api");
   }

   getNews(){
    // return this.http.get('http://127.0.0.1:8000/api/news');
    // return this.http.get('http://127.0.0.1:8000/list_news/');
    return this.http.get('http://127.0.0.1:8000/api/news/');
   }

   getNewsByDate(min_date : string, max_date: string){
    // http://127.0.0.1:8000/api/news/?min_date=2020-05-01&max_date=2020-08-10
     return this.http.get(`http://127.0.0.1:8000/api/news/?min_date=${min_date}&max_date=${max_date}&ordering=-country`);
   }
}
