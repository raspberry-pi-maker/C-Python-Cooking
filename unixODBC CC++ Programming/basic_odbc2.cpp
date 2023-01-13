#include <stdio.h>
#include <string.h>
#include <string>
#include <iostream>
#include <sql.h>
#include <sqlext.h>

using namespace std;

void debug_err(SQLRETURN rc, SQLHSTMT stmt){
    SQLLEN numRecs = 0;
    SQLSMALLINT   i, MsgLen;
    SQLRETURN     rc2; 
    SQLCHAR       SqlState[6], Msg[SQL_MAX_MESSAGE_LENGTH];
    SQLINTEGER    NativeError;  
    
    SQLGetDiagField(SQL_HANDLE_STMT, stmt, 0, SQL_DIAG_NUMBER, &numRecs, 0, 0);
    i = 1;  
    while (i <= numRecs && (rc2 = SQLGetDiagRec(SQL_HANDLE_STMT, stmt, i, SqlState, &NativeError,  
            Msg, sizeof(Msg), &MsgLen)) != SQL_NO_DATA) {  
        printf("SQLSTATE[%s] NATIVE ERROR[%d] Msg[%s]\n",SqlState,NativeError,Msg);
        i++;  
    }         
}

int main( int argc, char** argv ) {
    SQLHENV env;
    SQLHDBC dbc;
    SQLHSTMT stmt;
    SQLRETURN ret; /* ODBC API return status */
    SQLSMALLINT columns; /* number of columns in result-set */
    int row = 0;
    char sql[1024] = "";
    SQLRETURN rc1;
    string conn("DSN=myodbc");

    /* Allocate an environment handle */
    SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &env);
    /* We want ODBC 3 support */
    SQLSetEnvAttr(env, SQL_ATTR_ODBC_VERSION, (void *) SQL_OV_ODBC3, 0);
    /* Allocate a connection handle */
    SQLAllocHandle(SQL_HANDLE_DBC, env, &dbc);

    rc1 = SQLDriverConnect(dbc, NULL, (SQLCHAR*)conn.c_str(), SQL_NTS, NULL, 0, NULL, SQL_DRIVER_COMPLETE);
    if(SQL_SUCCESS != rc1){
        printf("SQLDriverConnect return [%d]\n", rc1);
    }
    /* Allocate a statement handle */
    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    /* execute a query */
    sprintf(sql, "select name, belong, phone from professor");
    rc1 = SQLExecDirect(stmt, (SQLCHAR*)sql, SQL_NTS);
    if(SQL_SUCCESS != rc1 && SQL_SUCCESS_WITH_INFO != rc1){
        debug_err(rc1, stmt);
        exit(0);
    }
    char name[36], belong[16], phone[16];
    SQLBindCol(stmt, 1, SQL_C_CHAR,  name, 32, NULL);
    SQLBindCol(stmt, 2, SQL_C_CHAR,  belong, 16, NULL);
    SQLBindCol(stmt, 3, SQL_C_CHAR,  phone, 16, NULL);


    for ( int i = 0; ; i++ ) {
        rc1 = SQLFetch( stmt );
        if ( rc1 == SQL_ERROR || rc1 != SQL_SUCCESS_WITH_INFO )
            debug_err(rc1, stmt);
        if ( rc1 == SQL_SUCCESS || rc1 == SQL_SUCCESS_WITH_INFO ) {
            cout << "Record [" << i + 1 << "]  ";
            cout << " name : " << name;
            cout << " belong : " << belong;
            cout << " \tphone : " << phone;
            cout << "\n";
        }
        else
            break;
    }
   
    rc1 = SQLFreeHandle( SQL_HANDLE_STMT, stmt );
    if(rc1 != SQL_SUCCESS){
        cout << "SQLFreeHandle (SQL_HANDLE_STMT)err:"<< rc1 << endl;
        exit(0);
    } 
    rc1 = SQLDisconnect( dbc );
    if(rc1 != SQL_SUCCESS){
        cout << "SQLDisconnect err:"<< rc1 << endl;
        exit(0);
    } 
    rc1 = SQLFreeHandle( SQL_HANDLE_DBC, dbc );
    if(rc1 != SQL_SUCCESS){
        cout << "SQLFreeHandle (SQL_HANDLE_DBC)err:"<< rc1 << endl;
        exit(0);
    } 
    rc1 = SQLFreeHandle( SQL_HANDLE_ENV, env );    
    if(rc1 != SQL_SUCCESS){
        cout << "SQLFreeHandle (SQL_HANDLE_ENV)err:"<< rc1 << endl;
        exit(0);
    } 
    cout << "basic odbc test end" << endl;    
    return 0;
}