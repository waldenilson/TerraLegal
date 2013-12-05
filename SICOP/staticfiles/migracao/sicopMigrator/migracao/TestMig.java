package br.gov.incra.migracao;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class TestMig {

	
	public static void main(String a[])
	{
//    	EntArea [] areas;

		
		Connection conexao = Conexao.getConexao();
		Statement statement;
		ResultSet resultSet;
		String sql = "select * from tbpecastecnicas";
		try{
	   		 statement = conexao.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_READ_ONLY);
	   		 resultSet = statement.executeQuery(sql);
		    	 resultSet.last();
		    	 int tamanho=resultSet.getRow();
		    	 System.out.println(tamanho);
	   		 resultSet.first();
	   	 }
	   	 catch(SQLException exception){
	   		 exception.printStackTrace();
	   	 }

		
//   	 areas = new EntArea[tamanho];
//   	 for(int i=0;i<tamanho;i++){
//   		 areas[i]=new EntArea();
//   		 try {
//				 areas[i].setCodigo(resultSet.getInt(1));
//				 areas[i].setNome(resultSet.getString(2));
//				 resultSet.next();
//			 } catch (SQLException exception) {
//				 exception.printStackTrace();
//			 }
//   	 }
//   	 return areas;

		
	}
}
