package br.gov.incra.migracao;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class MigracaoMovimentacao {

	private String diretorio = "C:\\DEVELOPER/SICOP/Migracao";
	private String nomeArqMigracao = "scriptTbmovimentacao.sql";
	private String nomeArqLegado = "dump_tbmovimentacao.txt";
	
	public MigracaoMovimentacao()
	{		
		File dir = new File( diretorio );
		String todosScripts = "";
			String conteudo = ler(diretorio, nomeArqLegado);
			todosScripts += conteudo;
		escreve(todosScripts, new File(dir, nomeArqMigracao) );
	}
	
	public static void main(String a[])
	{
		new MigracaoMovimentacao();
	}
		
	public String ler(String diretorio, String nomeArq)
	{
		
			File dir = new File( diretorio );
			File arq = new File(dir, nomeArq );
		 				
			try {
		        //Indicamos o arquivo que ser√° lido
		        FileReader fileReader = new FileReader(arq);
		 
		        //Criamos o objeto bufferReader que nos
		        // oferece o m√©todo de leitura readLine()
		        BufferedReader bufferedReader =
		            new BufferedReader(fileReader);
		 
		        //String que ir√° receber cada linha do arquivo
		        String linha = "";
		        String conteudo = "";
		        String tabela = nomeArq.substring(5, nomeArq.length()-4);
	//	        System.out.println("table: "+tabela);
		        String leitura = "";
		        
		        
		        
		        //Fazemos um loop linha a linha no arquivo,
		        // enquanto ele seja diferente de null.
		        //O m√©todo readLine() devolve a linha na
		        // posicao do loop para a variavel linha.
		        int x = 1; int lixo = 0;
		        List<String> errosnumero = new ArrayList<String>();
		        List<String> errosorigem = new ArrayList<String>();
		        List<String> errosdestino = new ArrayList<String>();
		        List<String> perfeita = new ArrayList<String>();
		        
//				LISTAS DAS COLUNAS
		        List<String> numero = new ArrayList<String>();
		        List<String> data = new ArrayList<String>();
		        List<String> origem = new ArrayList<String>();
		        List<String> destino = new ArrayList<String>();
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
		        		
		        		if(y==1) // data
		        		{
		        			data.add(aux);
		        		}

		        		if(y==2) // caixa origem
		        		{
		        			if(a.equals("TITULADOS ENTREGUES  3"))
		        				a = "TITULADOS ENTREGUES 03";
		        			if(a.equals("SIPRADO 1"))
		        				a = "SIPRADO 01";
		        			if(a.equals("DESPACHO CONJUR"))
		        				a = "DESPACHO PARA CONJUR";
		        			if(a.contains("AGUARDANDO PE«AS"))
		        				a = "AGUARDANDO PE«AS - 003";
		        			
		        			aux = (String) MigracaoAuxiliar.mapCaixa().get( a );
		        			if (aux == null)
		        			{
		        				aux = (String) MigracaoAuxiliar.mapCaixa().get( MigracaoAuxiliar.normalizarString(a) );
		        				if (aux == null )
		        					errosorigem.add("erro | "+a);
			        		}
		        			origem.add(aux);
		        		}
		        		if(y==3) // caixa destino
		        		{
		        			if(a.contains("AGUARDANDO PE«AS"))
		        				a = "AGUARDANDO PE«AS - 003";
		        			if(a.equals("SIPRADO 1"))
		        				a = "SIPRADO 01";
		        			if(a.equals("TITULADOS ENTREGUES  3"))
		        				a = "TITULADOS ENTREGUES 03";
		        			if(a.equals("DESPACHO CONJUR"))
		        				a = "DESPACHO PARA CONJUR";
		        			
		        			aux = (String) MigracaoAuxiliar.mapCaixa().get( a );
		        			if (aux == null)
		        			{
		        				aux = (String) MigracaoAuxiliar.mapCaixa().get( MigracaoAuxiliar.normalizarString(a) );
			        			if (aux == null )
		        					errosdestino.add("erro | "+a);
		        			}
			        		destino.add(aux);
		        		}

		        		if(y==4) // usuario
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
	        		String cont = numero.get(a)+", "+data.get(a)+", "+origem.get(a)+", "+
	        				destino.get(a)+", "+usuario.get(a)+", 0";
		        	
	 //        		cont = cont.replaceAll("\t\t", "\t");
	        		cont = cont.replaceAll("\t", ",");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll("''", "null");
	        		tabela = "tbmovimentacao";
	        		conteudo += "INSERT INTO "+tabela+" values( "+cont+" );\n";
		        	leitura += x+"\t"+"INSERT INTO "+tabela+" values( "+cont+" );\n";
		        }
		        System.out.println("conteudo: "+leitura);
		        
	//	        escreve(conteudo, new File(dir, "dump_"+tabela+"_db.sql") );
		 
		        //liberamos o fluxo dos objetos
		        // ou fechamos o arquivo
		        fileReader.close();
		        bufferedReader.close();

		        System.out.println("ERROS NUMERO: "+errosnumero.size()+
		        		"\nERROS ORIGEM: "+errosorigem.size()+
		        		"\nERROS DESTINO: "+errosdestino.size()+
		        		"\nERROS ORIGEM: "+errosorigem+
		        		"\nERROS DESTINO: "+errosdestino+
		        		"\nREGISTROS: "+x+
		        		"\nLIXOS: "+lixo+
		        		"\nREGISTROS PERFEITOS: "+perfeita.size()+"\n\n\n");


		        System.out.println("numero: "+numero.size()+
		        		"\n\n\n");


		        
		        return conteudo;
		    } catch (IOException e) {
		        e.printStackTrace();
		        return null;
		    }

	}
	
	// m√©todo para escrever no TXT  
    public void escreve (String conteudo, File arq){  
          
        try {  
            FileWriter escreve = new FileWriter(arq, true);  
            conteudo += System.getProperty("line.separator"); // pular linha  
            escreve.write(conteudo); // escrever o conte√∫do  
            escreve.close();  
        } catch (IOException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        }  
    }  
		
}
