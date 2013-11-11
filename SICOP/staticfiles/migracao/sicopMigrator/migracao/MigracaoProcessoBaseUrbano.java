package br.gov.incra.migracao;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class MigracaoProcessoBaseUrbano {

	private String diretorio = "c:\\DEVELOPER/SICOP/Migracao";
	private String nomeArqMigracao = "scriptTbprocessobase.sql";
	private String nomeArqLegado = "dump_tbprocessourbano.txt";
	
	public MigracaoProcessoBaseUrbano()
	{		
		File dir = new File( diretorio );
		String todosScripts = "";
			String conteudo = ler(diretorio, nomeArqLegado);
			todosScripts += conteudo;
		escreve(todosScripts, new File(dir, nomeArqMigracao) );
	}
	
	public static void main(String a[])
	{
		new MigracaoProcessoBaseUrbano();
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
		        List<String> errosmunicipios = new ArrayList<String>();
		        List<String> erroscaixa = new ArrayList<String>();
		        List<String> errosgleba = new ArrayList<String>();
		        List<String> errosclassificacao = new ArrayList<String>();
		        List<String> perfeita = new ArrayList<String>();

		        
//				LISTAS DAS COLUNAS
		        List<String> numero = new ArrayList<String>();
		        List<String> gleba = new ArrayList<String>();
		        List<String> caixa = new ArrayList<String>();
		        List<String> municipio = new ArrayList<String>();
		        List<String> usuario = new ArrayList<String>();
		        List<String> data = new ArrayList<String>();
		        List<String> classificacao = new ArrayList<String>();

		        
		        
		        while ( ( linha = bufferedReader.readLine() ) != null) {
		            
		        	//Aqui imprimimos a linha
	//	        	tabela = "tbconjuge";
		        	
	//	        	String cont = linha.replaceAll("\t", ",");
		        	String cont = linha;
		        	String contaux = "";
		        	String[] s = cont.split(";");
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

		        		if(y==0) // numero
		        		{
		        			numero.add(aux);
		        		}
		        		
		        		if(y==6) // data
		        		{
		        			data.add(aux);
		        		}

		        		if(y==16) // usuario
		        		{
		        			aux = (String) MigracaoAuxiliar.mapAuthUser().get( a );
		        			if (aux == null)
		        				aux = "1";
		        			usuario.add(aux);
		        		}
		        		
		        		if(y==4) // gleba
		        		{
		        			if(a.isEmpty() || a.equals("-"))
		        				a = "DADOS MIGRADOS GLEBA";

		        			if(a.equals("FAZ. VIT”RIA"))
	        					a = "Fazenda Vitoria";
	        				
	        				if(a.equals("JO¡ JURITI"))
	        					a = "JaÛ";
	        					
	        				if(a.toUpperCase().equals("¡rea Urbana e de Expans„o".toUpperCase()))
	        					a = "·rea urbana e expans„o";

	        				if(a.equals("14"))
	        					a = "Area Urbana de Expansao 14";
	        				
	        				if(a.equals("DATA MATINHA"))
	        					a = "Matinha";
//	        				
	        				if(a.equals("Novo Corrego Poranguet·"))
	        					a = "Novo CÛrrego Poranguet·";
	        				
	        				if(a.equals("ALEGRIA"))
	        					a = "Alegria Agua Viva";
	        			
	        				if(a.equals("GLEBA 12"))
	        					a = "12";

	        				if(a.equals("GLEBA  GURGEL"))
	        					a = "Gurgel";
	        				
	        				if(a.equals("Piquia / brej„o"))
	        					a = "piquia brejao";
	        			
	        				if(a.equals("GLEBA JURITI") || a.equals("GL. JURITI") || a.equals("GLEBA   JURITI") || a.equals("GL.   JURITI"))
	        					a = "Juriti";
	        			
	        				
		        			aux = (String) MigracaoAuxiliar.mapGleba().get( a.toUpperCase() );
		        			if (aux == null)
		        			{
		        				errosgleba.add("erro-gleba");
		        				gleba.add(aux+" - "+a+" | "+x);
		        			}
		        			else
		        				gleba.add(aux);
		        		}
		        		if(y==5) // caixa
		        		{
		        			if(a.equals("SIPRADO 1"))
		        				a = "SIPRADO 01";
		        			if(a.equals("URBANO COM PENDENCIAS DE DOCUMENTOS 01"))
		        				a = "URBANO COM PEND NCIA DE DOCUMENTO 01";
		        			if(a.isEmpty() || a.equals("-"))
		        				a = "DADOS MIGRADOS URBANO";
		        			aux = (String) MigracaoAuxiliar.mapCaixa().get( a );
		        			if (aux == null)
		        			{
		        				erroscaixa.add("erro-caixa | "+a);
		        				caixa.add(aux);
		        			}
		        			else
		        				caixa.add(aux);
		        		}
		        		if(y==1) // municipio
		        		{
		        			aux = (String) MigracaoAuxiliar.mapMunicipio().get(  MigracaoAuxiliar.normalizarString(a.toUpperCase()) );
		        			if (aux == null)
		        				errosmunicipios.add("erro-municipio");
		        			municipio.add(aux);
		        		}
		        		
		        		if(y==12) // classificacaoprocesso
		        		{
//		        			if(a.equals("pai"))
		        			aux = "1";
//		        			else if(a.equals("anexo"))
//		        				aux = "2";
//		        			else
//		        				errosclassificacao.add("erro-classificacao");
		        			classificacao.add(aux);
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
	        		// verificar se o processo eh anexo
        			String res = (String) MigracaoAuxiliar.mapProcessosAnexos().get( numero.get(a) );
        			if (res == null)
        			{
        				classificacao.set(a, "1");
        			}
        			else
        				classificacao.set(a, "2");

	        		int id = a+1;
	        		String cont = numero.get(a)+", "+gleba.get(a)+", "+caixa.get(a)+", "+
	        				municipio.get(a)+", "+usuario.get(a)+", "+"3, 1, "+data.get(a)+", "+classificacao.get(a)+", 1";
		        	
	 //        		cont = cont.replaceAll("\t\t", "\t");
	        		cont = cont.replaceAll("\t", ",");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll("''", "null");
	        		tabela = "tbprocessobase";
	        		conteudo += "INSERT INTO "+tabela+" values( "+cont+" );\n";
		        	leitura += x+"\t"+"INSERT INTO "+tabela+" values( "+cont+" );\n";
		        }
		        System.out.println("conteudo: "+leitura);
		        
	//	        escreve(conteudo, new File(dir, "dump_"+tabela+"_db.sql") );
		 
		        //liberamos o fluxo dos objetos
		        // ou fechamos o arquivo
		        fileReader.close();
		        bufferedReader.close();

		        System.out.println("ERROS MUNICIPIOS: "+errosmunicipios.size()+
		        		"\nERROS CAIXA: "+erroscaixa.size()+
		        		"\nERROS GLEBA: "+errosgleba.size()+
		        		"\nERROS CLASSIFICACAO: "+errosclassificacao.size()+
		        		"\nREGISTROS: "+x+
		        		"\nLIXOS: "+lixo+
		        		"\nREGISTROS PERFEITOS: "+perfeita.size()+"\n\n\n");


		        System.out.println("numero: "+numero.size()+
		        		"\ncaixa: "+caixa.size()+
		        		"\ngleba: "+gleba.size()+
		        		"\ndata: "+data.size()+
		        		"\nusuario: "+usuario.size()+
		        		"\nclassificacao: "+classificacao.size()+
		        		"\nmunicipio: "+municipio.size()+"\n\n\n");

		        System.out.println("Caixa: "+erroscaixa);

		        
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
