package br.gov.incra.migracao;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class MigracaoPendencia {

	private String diretorio = "C:\\DEVELOPER/SICOP/Migracao";
	private String nomeArqMigracao = "scriptTbpendencia.sql";
	private String nomeArqLegado = "dump_tbpendencia.txt";
	
	public MigracaoPendencia()
	{		
		File dir = new File( diretorio );
		String todosScripts = "";
			String conteudo = ler(diretorio, nomeArqLegado);
			todosScripts += conteudo;
		escreve(todosScripts, new File(dir, nomeArqMigracao) );
	}
	
	public static void main(String a[])
	{
		new MigracaoPendencia();
	}
		
	public String ler(String diretorio, String nomeArq)
	{
		
			File dir = new File( diretorio );
			File arq = new File(dir, nomeArq );
		 				
			try {
		        //Indicamos o arquivo que será lido
		        FileReader fileReader = new FileReader(arq);
		 
		        //Criamos o objeto bufferReader que nos
		        // oferece o método de leitura readLine()
		        BufferedReader bufferedReader =
		            new BufferedReader(fileReader);
		 
		        //String que irá receber cada linha do arquivo
		        String linha = "";
		        String conteudo = "";
		        String tabela = nomeArq.substring(5, nomeArq.length()-4);
	//	        System.out.println("table: "+tabela);
		        String leitura = "";
		        
		        
		        
		        //Fazemos um loop linha a linha no arquivo,
		        // enquanto ele seja diferente de null.
		        //O método readLine() devolve a linha na
		        // posicao do loop para a variavel linha.
		        int x = 1; int lixo = 0;
		        List<String> errosnumero = new ArrayList<String>();
		        List<String> errostipo = new ArrayList<String>();
		        List<String> errosusuario = new ArrayList<String>();
		        List<String> errosstatus = new ArrayList<String>();
		        List<String> perfeita = new ArrayList<String>();

		        
//				LISTAS DAS COLUNAS
		        List<String> numero = new ArrayList<String>();
		        List<String> tipo = new ArrayList<String>();
		        List<String> descricao = new ArrayList<String>();
		        List<String> data = new ArrayList<String>();
		        List<String> usuario = new ArrayList<String>();
		        List<String> status = new ArrayList<String>();
		        
		        
		        
		        while ( ( linha = bufferedReader.readLine() ) != null) {
		         

		        	//Aqui imprimimos a linha
	//	        	tabela = "tbconjuge";
		        	
	//	        	String cont = linha.replaceAll("\t", ",");
		        	String cont = linha;
		        	String contaux = "";
		        	String[] s = cont.split("|");

		        	if(s.length != 7)
		        		perfeita.add("ok");

		        	for(int y=0; y < s.length ; y++)
		        	{
		        		String aux = "";
		        		String a = s[y];
		        		
		        		a = a.replaceAll("\"", "");
		        		a = a.trim();
		        		
		        		if (a.startsWith("20") && a.contains("-") && a.contains(":"))
		        			aux = "'"+a+"'";
	
		        		else if (a.startsWith("{") && a.endsWith("}") )
		        			aux = "'"+a+"'";
		        		
		        		else
		        		
		        			aux = "'"+a+"'";

		        		if(y==1) // numero
		        		{
		        			if(a.equals("5641800036620988"))
		        				a = "56418000366200988";
		        			
		        			aux = (String) MigracaoAuxiliar.mapProcessoBase().get( a );
		        			if (aux == null)
		        				errosnumero.add("erros | "+a);
		        			numero.add(aux);
		        		}

		        		if(y==2) // tipo
		        		{
//		        			aux = (String) MigracaoAuxiliar.mapTipoPendencia().get( a );
//		        			if (aux == null)
//		        				errostipo.add("erros | "+a);
		        			aux = aux.replace("'", "");
		        			tipo.add(aux);
		        		}

		        		if(y==3) // descricao
		        		{
		        			descricao.add(aux);
		        		}

		        		if(y==4) // data
		        		{
		        			data.add(aux);
		        		}

		        		if(y==5) // usuario
		        		{
		        			aux = (String) MigracaoAuxiliar.mapAuthUser().get( a );
		        			if (aux == null)
		        				aux = "1";
		        			usuario.add(aux);
		        		}
		
		        		if(y==6) // status
		        		{
		        			if(a.toUpperCase().equals("SANADO"))
		        				aux = "1";
		        			else if(a.toUpperCase().equals("PENDENTE"))
		        				aux = "2";
		        			aux = aux.replaceAll("'", "");
		        			status.add(aux);
		        		}
		        				        					        		
		        		contaux += aux+"\t";
		        		
		        	}
//		        	cont = contaux.substring(0,contaux.length()-1);
		        			        	
		        	
//		        	System.out.println( cont );
	//	        	System.exit(0);
	//	        	cont = cont.replaceAll("\t", ",");
		        	
		        	x++;
	//	            System.out.println(conteudo);
		        }
		        for( int a=0; a<numero.size();a++)
	        	{

	        		int id = a+1;
	        		String cont = "0, "+numero.get(a)+", "+tipo.get(a)+", "+descricao.get(a)+", "+
	        				data.get(a)+", "+usuario.get(a)+", "+status.get(a);
		        	        		
	 //        		cont = cont.replaceAll("\t\t", "\t");
	        		cont = cont.replaceAll("\t", ",");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll(",,", ",null,");
//	        		cont = cont.replaceAll("''", "null");
	        		tabela = "tbpendencia";
	        		conteudo += "INSERT INTO "+tabela+" values( "+cont+" );\n";
		        	leitura += x+"\t"+"INSERT INTO "+tabela+" values( "+cont+" );\n";
		        }
		        System.out.println("conteudo: "+leitura);
		        
	//	        escreve(conteudo, new File(dir, "dump_"+tabela+"_db.sql") );
		 
		        //liberamos o fluxo dos objetos
		        // ou fechamos o arquivo
		        fileReader.close();
		        bufferedReader.close();

		        System.out.println("ERROS NUMERO: "+errosnumero+
		        		"\nERROS TIPO: "+errostipo.size()+
		        		"\nERROS USUARIO: "+errosusuario.size()+
		        		"\nREGISTROS: "+x+
		        		"\nLIXOS: "+lixo+
		        		"\nREGISTROS PERFEITOS: "+perfeita.size()+"\n\n\n");


		        System.out.println("numero: "+numero.size()+
		        		"\ntipo: "+tipo.size()+
		        		"\ndata: "+data.size()+
		        		"\nusuario: "+usuario.size()+
		        		"\nstatus: "+status.size()+"\n\n\n");


		        
		        return conteudo;
		    } catch (IOException e) {
		        e.printStackTrace();
		        return null;
		    }

	}
	
	// método para escrever no TXT  
    public void escreve (String conteudo, File arq){  
          
        try {  
            FileWriter escreve = new FileWriter(arq, true);  
            conteudo += System.getProperty("line.separator"); // pular linha  
            escreve.write(conteudo); // escrever o conteúdo  
            escreve.close();  
        } catch (IOException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        }  
    }  
		
}
