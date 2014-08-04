package br.gov.incra.migracao;

import java.sql.*;

public final class Conexao
{
   private static Connection conexao;
   
   private Conexao(){
	   try{
           conexao = DriverManager.getConnection("jdbc:postgresql://localhost/dbprocessosdev","postgres","postgres");
       }
       catch(SQLException exception){
           exception.printStackTrace();
       }
   }
   
   public static Connection getConexao() {
	   if (conexao == null) {
		   new Conexao();
	   }
	   return conexao;
   }
   
   public static void desconecta(){
       if (conexao!=null){
    	   try{
    		   conexao.close();
    		   conexao=null;
    	   }
    	   catch(SQLException exception){
    		   exception.printStackTrace();
    	   }
       }
   }
}
