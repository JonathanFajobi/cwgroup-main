export interface RequestOptions {
    qParams?: string | Record<string, string>;
    body?: any;
    id?: string | null;
}

export type Friend = {
    id: number;
    username: string; 
    age: number;
    hobbies: Set<string>;
    matching: number;  
}

export type Request = {
    id: number;
    username: string;
    firstName: string; 
    lastName: string;
    // This is the ID of the account that has been requested to for Janoth and Luke
    userId: string;
}

export type User = {
    id: number | null;
    username: string;
    firstName: string; 
    lastName: string;
    email: string; 
    dob: Date;
    hobbies: Set<string>;
    matching: undefined | null | number; 
}
