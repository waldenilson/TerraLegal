package br.gov.incra.migracao;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class MigracaoProcessosAnexos {

	private String diretorio = "C:\\DEVELOPER/SICOP/Migracao";
	private String nomeArqMigracao = "scriptTbprocessosanexos.sql";
	private String nomeArqLegado = "dump_tbprocessosanexos.txt";
	
	public MigracaoProcessosAnexos()
	{		
		File dir = new File( diretorio );
		String todosScripts = "";
			String conteudo = ler(diretorio, nomeArqLegado);
			todosScripts += conteudo;
		escreve(todosScripts, new File(dir, nomeArqMigracao) );
	}
	
	public static void main(String a[])
	{
		new MigracaoProcessosAnexos();
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
		        List<String> errosanexo = new ArrayList<String>();
		        List<String> errosusuario = new ArrayList<String>();
		        List<String> perfeita = new ArrayList<String>();
		        
//				LISTAS DAS COLUNAS
		        List<String> numero = new ArrayList<String>();
		        List<String> anexo = new ArrayList<String>();
		        List<String> data = new ArrayList<String>();
		        List<String> usuario = new ArrayList<String>();
		        
		        while ( ( linha = bufferedReader.readLine() ) != null) {
		            
		        	//Aqui imprimimos a linha
	//	        	tabela = "tbconjuge";
		        	
	//	        	String cont = linha.replaceAll("\t", ",");
		        	String cont = linha;
		        	String contaux = "";
		        	String[] s = cont.split("\t");
		        	for(int y=0; y < s.length ; y++)
		        	{
		        		String aux = "";
		        		String a = s[y];
		        		
		        		a = a.replaceAll("'", "");
		        		a = a.trim();
		        		
		        		if (a.startsWith("20") && a.contains("-") && a.contains(":"))
		        			aux = "'"+a+"'";
	
		        		else if (a.startsWith("{") && a.endsWith("}") )
		        			aux = "'"+a+"'";
		        		
		        		else
		        			aux = "'"+a+"'";

		        		if(y==0) // numero
		        		{
		        			aux = (String) MigracaoAuxiliar.mapProcessoBase().get( a );
		        			if (aux == null)
		        				errosnumero.add("erro");
		        			numero.add(aux);
		        		}
		        		
		        		if(y==2) // data
		        		{
		        			data.add(aux);
		        		}

		        		if(y==1) // anexo
		        		{
		        			aux = (String) MigracaoAuxiliar.mapProcessoBase().get( a );
		        			if (aux == null)
		        				errosanexo.add("erro | "+a);
		        			anexo.add(aux);
		        		}

		        		if(y==3) // usuario
		        		{
		        			aux = (String) MigracaoAuxiliar.mapAuthUser().get( a );
		        			if (aux == null)
		        				aux = "1";
		        			usuario.add(aux);
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
	        		String cont = numero.get(a)+", "+anexo.get(a)+", "+
	        				data.get(a)+", "+usuario.get(a);
		        	
	 //        		cont = cont.replaceAll("\t\t", "\t");
	        		cont = cont.replaceAll("\t", ",");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll("''", "null");
	        		tabela = "tbprocessosanexos";
	        		if(anexo.get(a).equals("null"))
		        	{
	        			conteudo += "INSERT INTO "+tabela+" values( "+cont+" );\n";
		        		leitura += x+"\t"+"INSERT INTO "+tabela+" values( "+cont+" );\n";
		        	}
		        }
		        System.out.println("conteudo: "+leitura);
		        
	//	        escreve(conteudo, new File(dir, "dump_"+tabela+"_db.sql") );
		 
		        //liberamos o fluxo dos objetos
		        // ou fechamos o arquivo
		        fileReader.close();
		        bufferedReader.close();

		        System.out.println("ERROS NUMERO: "+errosnumero.size()+
		        		"\nERROS ANEXO: "+errosanexo.size()+
		        		"\nERROS USUARIO: "+errosusuario.size()+
		        		"\nREGISTROS: "+x+
		        		"\nLIXOS: "+lixo+
		        		"\nREGISTROS PERFEITOS: "+perfeita.size()+"\n\n\n");

		        System.out.println("numero: "+numero.size()+
		        		"Anexo: "+errosanexo+
		        		"\n\n\n");
		        
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
